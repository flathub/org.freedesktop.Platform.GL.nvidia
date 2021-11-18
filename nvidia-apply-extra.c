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

int nvidia_major_version;

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
        die_with_libarchive (ar, "archive_write_data_block: %s");

      r = archive_write_data_block (aw, buff, size, offset);
      if (r != ARCHIVE_OK)
        die_with_libarchive (aw, "archive_write_data_block: %s");
    }
}

static int
should_extract (struct archive_entry *entry)
{
  const char *path = archive_entry_pathname (entry);
  int is_compat32 = 0;

  if (has_prefix (path, "./"))
    path += 2;

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

#ifdef __i386__
  /* Nvidia no longer has 32bit drivers so we are getting
   * the 32bit compat libs from the 64bit drivers */
  if (nvidia_major_version > 390)
    {
      if (!has_prefix (path, "32/"))
        return 0;
      is_compat32 = 1;
      path += 3;
    }
#endif

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
      strstr (path, "egl-gbm"))
    {
      if (is_compat32)
        archive_entry_set_pathname (entry, path);
      return 1;
    }

  if ((has_prefix (path, "lib") ||
       has_prefix (path, "tls/lib"))&&
      has_suffix (path, ".so." NVIDIA_VERSION))
    {
      if (is_compat32)
        archive_entry_set_pathname (entry, path);
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
  char buffer[1024];
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

  nvidia_major_version = atoi (NVIDIA_VERSION);

  fd = open (NVIDIA_BASENAME, O_RDONLY);
  if (fd == -1)
    die_with_error ("open extra data");

  skip_lines = find_skip_lines (fd);
  tar_start = find_line_offset (fd, skip_lines);

  if (lseek (fd, tar_start, SEEK_SET)!= tar_start)
    die ("Can't seek to tar");

  extract (fd);

  close (fd);

  unlink (NVIDIA_BASENAME);

  char *ldconfig_argv[] = {"ldconfig", "-n", ".", NULL};
  if (subprocess (ldconfig_argv))
    die ("running ldconfig failed");

  if (nvidia_major_version >= 470)
    {
      symlink ("libnvidia-vulkan-producer.so." NVIDIA_VERSION, "libnvidia-vulkan-producer.so");
    }

  symlink ("libcuda.so.1", "libcuda.so");
  symlink ("libnvidia-ml.so.1", "libnvidia-ml.so");

  if (nvidia_major_version >= 495)
    {
      mkdir ("gbm", 0755);
      symlink ("../libnvidia-allocator.so." NVIDIA_VERSION, "gbm/nvidia-drm_gbm.so");
    }

  mkdir ("OpenCL", 0755);
  mkdir ("OpenCL/vendors", 0755);
  create_file_with_content ("OpenCL/vendors/nvidia.icd", "libnvidia-opencl.so");

  if (nvidia_major_version > 340)
    replace_string_in_file ("vulkan/icd.d/nvidia_icd.json",
                            "__NV_VK_ICD__", "libGLX_nvidia.so.0");

  return 0;
}
