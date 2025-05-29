#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <archive.h>
#include <archive_entry.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>
#include <linux/limits.h>

int nvidia_major_version = 0;
int nvidia_minor_version = 0;
int nvidia_patch_version = 0;
int embedded_installer = 0;

void
die_with_error (const char *format, ...)
{
  va_list args;
  int errsv;

  errsv = errno;

  va_start (args, format);
  vfprintf (stderr, format, args);
  va_end (args);

  fprintf (stderr, ": %s\n", strerror (errsv));

  exit (1);
}

void
die_with_libarchive (struct archive *ar, const char *format)
{
  fprintf (stderr, format, archive_error_string (ar));
  exit (1);
}

void
die (const char *format, ...)
{
  va_list args;

  va_start (args, format);
  vfprintf (stderr, format, args);
  va_end (args);

  fprintf (stderr, "\n");

  exit (1);
}

int
parse_driver_version (const char *version,
                      int *major,
                      int *minor,
                      int *patch)
{
  return sscanf(version, "%d.%d.%d", major, minor, patch) < 2;
}

void
checked_symlink (const char *target,
                 const char *linkpath)
{
  if (symlink (target, linkpath) != 0)
    die_with_error ("failed to symlink '%s' to '%s'", target, linkpath);
  if (access (linkpath, F_OK) != 0 && errno == ENOENT)
    die ("broken symlink: '%s' points to a missing file", linkpath);
}

static int
has_prefix (const char *str,
            const char *prefix)
{
  return strncmp (str, prefix, strlen (prefix)) == 0;
}

static int
has_suffix (const char *str, const char *suffix)
{
  int str_len;
  int suffix_len;

  str_len = strlen (str);
  suffix_len = strlen (suffix);

  if (str_len < suffix_len)
    return 0;

  return strcmp (str + str_len - suffix_len, suffix) == 0;
}

static void
copy_archive (struct archive *ar,
              struct archive *aw)
{
  int r;
  const void *buff;
  size_t size;
  int64_t offset;

  while (1)
    {
      r = archive_read_data_block (ar, &buff, &size, &offset);
      if (r == ARCHIVE_EOF)
        break;
      if (r != ARCHIVE_OK)
        die_with_libarchive (ar, "archive_read_data_block: %s");

      r = archive_write_data_block (aw, buff, size, offset);
      if (r != ARCHIVE_OK)
        die_with_libarchive (aw, "archive_write_data_block: %s");
    }
}

static int
should_extract (struct archive_entry *entry)
{
  const char *path = archive_entry_pathname (entry);
  char new_path[PATH_MAX];

  if (has_prefix (path, "./"))
    path += 2;

  /* Ignore the '32' directory (32-bit only libraries) when extracting on non-GL32. */
  if (strcmp (ARCH, "i386") != 0 && has_prefix (path, "32/"))
    return 0;

  /* this tar is only a container that stores the actual driver .run file */
  if (has_suffix (path, ".run"))
    {
      archive_entry_set_pathname (entry, "./embedded_installer.run");
      embedded_installer = 1;
      return 1;
    }

  if (strcmp (path, "nvidia_icd.json") == 0 || strcmp (path, "nvidia_icd.json.template") == 0)
    {
      archive_entry_set_pathname (entry, "./vulkan/icd.d/nvidia_icd.json");
      return 1;
    }
  if (strcmp (path, "nvidia_layers.json") == 0)
    {
      archive_entry_set_pathname (entry, "./vulkan/implicit_layer.d/nvidia_layers.json");
      return 1;
    }
  if (strcmp (path, "10_nvidia.json") == 0)
    {
      archive_entry_set_pathname (entry, "./glvnd/egl_vendor.d/10_nvidia.json");
      return 1;
    }
  if (strcmp (path, "10_nvidia_wayland.json") == 0)
    {
      archive_entry_set_pathname (entry, "./egl/egl_external_platform.d/10_nvidia.json");
      return 1;
    }
  if (strcmp (path, "15_nvidia_gbm.json") == 0)
    {
      archive_entry_set_pathname (entry, "./egl/egl_external_platform.d/15_nvidia_gbm.json");
      return 1;
    }
  if (strcmp (path, "20_nvidia_xcb.json") == 0)
    {
      archive_entry_set_pathname (entry, "./egl/egl_external_platform.d/20_nvidia_xcb.json");
      return 1;
    }
  if (strcmp (path, "20_nvidia_xlib.json") == 0)
    {
      archive_entry_set_pathname (entry, "./egl/egl_external_platform.d/20_nvidia_xlib.json");
      return 1;
    }
  if (strcmp (path, "nvidia_icd_vksc.json") == 0)
    {
      archive_entry_set_pathname (entry, "./vulkansc/icd.d/nvidia_icd_vksc.json");
      return 1;
    }
  if ((strcmp (path, "nvidia-application-profiles-" NVIDIA_VERSION "-key-documentation") == 0) ||
      (strcmp (path, "nvidia-application-profiles-" NVIDIA_VERSION "-rc") == 0))
    {
      snprintf (new_path, sizeof new_path, "./share/nvidia/%s", path);
      archive_entry_set_pathname (entry, new_path);
      return 1;
    }
  if (strcmp (path, "nvoptix.bin") == 0)
    {
      snprintf (new_path, sizeof new_path, "./share/nvidia/%s", path);
      archive_entry_set_pathname (entry, new_path);
      return 1;
    }

  /* Nvidia no longer has 32bit drivers so we are getting
   * the 32bit compat libs from the 64bit drivers */
  if (strcmp (ARCH, "i386") == 0 && nvidia_major_version > 390)
    {
      if (!has_prefix (path, "32/"))
        return 0;
      path += 3;
    }

  /* Skip these as we're using GLVND on majod > 367*/
  if (nvidia_major_version > 367 &&
      (has_prefix (path, "libGL.so") ||
       has_prefix (path, "libEGL.so")))
    return 0;

  /* Skip these as we don't ship nvidia-settings */
  if (has_prefix (path, "libnvidia-gtk"))
    return 0;

  /* These are not versioned after the driver version */
  if (strstr (path, "egl-wayland") ||
      strstr (path, "egl-gbm") ||
      strstr (path, "egl-xcb") ||
      strstr (path, "egl-xlib") ||
      strstr (path, "libnvidia-api") ||
      strstr (path, "libnvidia-nvvm70"))
    {
      snprintf (new_path, sizeof new_path, "./lib/%s", path);
      archive_entry_set_pathname (entry, new_path);
      return 1;
    }

  if ((has_prefix (path, "lib") ||
       has_prefix (path, "tls/lib"))&&
      has_suffix (path, ".so." NVIDIA_VERSION))
    {
      snprintf (new_path, sizeof new_path, "./lib/%s", path);
      archive_entry_set_pathname (entry, new_path);
      return 1;
    }

  if (has_suffix (path, ".dll"))
    {
      snprintf (new_path, sizeof new_path, "./lib/nvidia/wine/%s", path);
      archive_entry_set_pathname (entry, new_path);
      return 1;
    }

  return 0;
}

static void
extract (int fd)
{
  struct archive *a;
  struct archive *ext;
  struct archive_entry *entry;
  int r;

  a = archive_read_new ();
  ext = archive_write_disk_new ();
  archive_read_support_format_tar (a);
  archive_read_support_filter_xz (a);
  archive_read_support_filter_gzip (a);
  archive_read_support_filter_zstd (a);

  if ((r = archive_read_open_fd (a, fd, 16*1024)))
    die_with_libarchive (a, "archive_read_open_fd: %s");

  while (1)
    {
      r = archive_read_next_header (a, &entry);
      if (r == ARCHIVE_EOF)
        break;

      if (r != ARCHIVE_OK)
        die_with_libarchive (a, "archive_read_next_header: %s");

      if (!should_extract (entry))
        continue;

      r = archive_write_header (ext, entry);
      if (r != ARCHIVE_OK)
        die_with_libarchive (ext, "archive_write_header: %s");
      else
        {
          copy_archive (a, ext);
          r = archive_write_finish_entry (ext);
          if (r != ARCHIVE_OK)
            die_with_libarchive (ext, "archive_write_finish_entry: %s");
        }
    }

  archive_read_close (a);
  archive_read_free (a);

  archive_write_close (ext);
  archive_write_free (ext);
}

static int
find_skip_lines (int fd)
{
  /*
   * CUDA drivers use makeself v2.1.4, which doesn't have a skip= line at the
   * beginning of the file. Instead, there's an
   * offset=`head -n "$skip" "$0" | wc -c | tr -d " "`
   * after all of the `--help` text, at approx the 14k byte offset.
   *
   * See https://github.com/megastep/makeself/commit/0d093c01e06ee76643ba2cffabf2ca07282d3af1
   */
  char buffer[16*1024];
  ssize_t size;
  char *line_start, *line_end, *buffer_end;
  char *skip_str = NULL;
  int skip_lines;

  size = pread (fd, buffer, sizeof buffer - 1, 0);
  if (size == -1)
    die_with_error ("read extra data");

  buffer[size] = 0; /* Ensure zero termination */
  buffer_end = buffer + size;

  line_start = buffer;
  while (line_start < buffer_end)
    {
      line_end = strchr (line_start, '\n');
      if (line_end != NULL)
        {
          *line_end = 0;
          line_end += 1;
        }
      else
        line_end = buffer_end;

      if (has_prefix (line_start, "skip="))
        {
          skip_str = line_start + 5;
          break;
        }
      else if (has_prefix (line_start, "offset=`head -n "))
        /* makeself v2 removed the skip= line, then added it back in v2.4.2 */
        {
          skip_str = line_start + 16;
          skip_lines = atoi (skip_str);
          if (skip_lines == 0)
            die ("Can't parse offset=`head -n %s", skip_str);

          return skip_lines + 1;
        }

      line_start = line_end;
    }

  if (skip_str == NULL)
    die ("Can't find skip size");

  skip_lines = atoi (skip_str);

  if (skip_lines == 0)
    die ("Can't parse skip=%s", skip_str);

  return skip_lines;
}

static off_t
find_line_offset (int fd, int skip_lines)
{
  off_t offset, buf_offset;
  int n_lines;
  ssize_t size;
  char buffer[16*1024];

  offset = 0;
  buf_offset = 0;
  n_lines = 1;

  while (1)
    {
      size = pread (fd, buffer, sizeof buffer, offset);
      if (size == -1)
        die_with_error ("read data");

      buf_offset = 0;
      while (buf_offset < size)
        {
          if (buffer[buf_offset] == '\n')
            {
              n_lines ++;
              if (n_lines == skip_lines)
                return offset + buf_offset + 1;
            }

          buf_offset++;
        }

      offset += size;
    }

  /* Should not happen */
  return 0;
}

static void
replace_string_in_file (const char *path,
                        const char *string,
                        const char *replacement)
{
  char *buffer, *p;
  size_t len;
  long fsize;
  FILE *f;

  if ((f = fopen (path, "r+")) == NULL)
    die_with_error ("reading file %s", path);

  fseek (f, 0, SEEK_END);
  fsize = ftell (f);
  fseek (f, 0, SEEK_SET);

  if ((buffer = malloc (fsize + 1)) == NULL)
    die ("out of memory");

  if ((len = fread (buffer, 1, fsize, f)) != fsize)
    die ("failed to read file %s", path);
  buffer[len] = '\0';

  if ((p = strstr (buffer, string)) != NULL)
    {
      char *new_buffer;
      size_t new_len, idx;

      new_len = len - strlen (string) + strlen (replacement) + 1;
      if ((new_buffer = malloc (new_len)) == NULL)
        die ("out of memory");

      idx = p - buffer;
      memmove (new_buffer, buffer, idx);
      new_buffer[idx] = '\0';

      strcat (new_buffer, replacement);
      idx += strlen (string);

      strcat (new_buffer, buffer + idx);

      fseek (f, 0, SEEK_SET);
      if (fwrite (new_buffer, 1, new_len - 1, f) != new_len - 1)
        die ("failed to write file %s", path);

      free (new_buffer);
    }

  free (buffer);
  fclose (f);
}

static void create_file_with_content(const char *path,
                                     const char *string)
{
  FILE *f;

  if ((f = fopen (path, "w+")) == NULL)
    die_with_error ("creating file %s", path);

  if (fprintf(f, "%s\n", string) != strlen(string) + 1)
    die ("failed to write to file %s", path);

  fclose (f);
}

static int
subprocess (char *const argv[])
{
  pid_t pid = fork ();
  int status;
  if (pid < 0)
    die_with_error ("failed to fork");
  else if (pid > 0)
    waitpid (pid, &status, WAIT_MYPGRP);
  else
    if (execvp (argv[0], argv) == -1)
      die_with_error ("exec failed: %s", argv[0]);
  return status;
}

int
main (int argc, char *argv[])
{
  int fd;
  int skip_lines;
  off_t tar_start;

  if (argc < 2)
    {
      fprintf (stderr, "usage: ./%s <path to NVIDIA installer>\n", argv[0]);
      return 1;
    }
  const char *nvidia_installer_path = argv[1];

  if (parse_driver_version (NVIDIA_VERSION,
                            &nvidia_major_version,
                            &nvidia_minor_version,
                            &nvidia_patch_version))
    die ("failed to parse driver version '%s'.", NVIDIA_VERSION);

  fd = open (nvidia_installer_path, O_RDONLY);
  if (fd == -1)
    die_with_error ("opening installer");

  skip_lines = find_skip_lines (fd);
  tar_start = find_line_offset (fd, skip_lines);

  if (lseek (fd, tar_start, SEEK_SET)!= tar_start)
    die ("Can't seek to tar");

  extract (fd);

  close (fd);

  /* check if this container is just a wrapper over the real driver container */
  if (access ("embedded_installer.run", F_OK) == 0)
    {
      if (embedded_installer)
        {
          /* marks it for deletion after it gets extracted */
          embedded_installer = 0;
          argv[1] = "embedded_installer.run";
          return main (argc, argv);
        }
      else
        {
          unlink ("embedded_installer.run");
        }
    }

  char *ldconfig_argv[] = {"ldconfig", "-n", "lib", NULL};
  if (subprocess (ldconfig_argv))
    die ("running ldconfig failed");

  if (((nvidia_major_version == 470 && nvidia_minor_version >= 63) ||
      nvidia_major_version >= 495) && nvidia_major_version < 545 &&
      strcmp(ARCH, "i386") != 0)
    {
      checked_symlink ("libnvidia-vulkan-producer.so." NVIDIA_VERSION,
                       "lib/libnvidia-vulkan-producer.so");
    }

  if (nvidia_major_version >= 550)
    {
      checked_symlink ("libnvidia-gpucomp.so." NVIDIA_VERSION, "lib/libnvidia-gpucomp.so");
    }

  checked_symlink ("libcuda.so.1", "lib/libcuda.so");
  checked_symlink ("libnvidia-ml.so.1", "lib/libnvidia-ml.so");
  checked_symlink ("libnvidia-opencl.so.1", "lib/libnvidia-opencl.so");
  checked_symlink ("libvdpau_nvidia.so.1", "lib/libvdpau_nvidia.so");

  if (nvidia_major_version >= 495)
    {
      mkdir ("lib/gbm", 0755);
      checked_symlink ("../libnvidia-allocator.so." NVIDIA_VERSION, "lib/gbm/nvidia-drm_gbm.so");
    }

  if (nvidia_major_version >= 319)
    {
      checked_symlink ("nvidia-application-profiles-" NVIDIA_VERSION "-key-documentation",
                       "share/nvidia/nvidia-application-profiles-key-documentation");
      checked_symlink ("nvidia-application-profiles-" NVIDIA_VERSION "-rc",
                       "share/nvidia/nvidia-application-profiles-rc");
    }

  if (nvidia_major_version <= 390)
    {
      unlink ("lib/libnvidia-tls.so." NVIDIA_VERSION);
      checked_symlink ("tls/libnvidia-tls.so." NVIDIA_VERSION,
                       "lib/libnvidia-tls.so." NVIDIA_VERSION);
    }

  mkdir ("OpenCL", 0755);
  mkdir ("OpenCL/vendors", 0755);
  create_file_with_content ("OpenCL/vendors/nvidia.icd", "libnvidia-opencl.so");

  if (nvidia_major_version > 340)
    replace_string_in_file ("vulkan/icd.d/nvidia_icd.json",
                            "__NV_VK_ICD__", "libGLX_nvidia.so.0");

  return 0;
}
