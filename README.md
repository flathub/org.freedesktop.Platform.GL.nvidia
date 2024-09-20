# To add a new driver

- Edit `versions.sh`, add new driver version.
- Run `update-data.sh`

The script will download the drivers from the nvidia servers and place the
 corresponding files in the `data` directory.

# Building locally

**1\.** Install the following packages:

```bash
flatpak-builder git make
```

**2\.** Add the Flathub repository:

```bash
flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

**3\.** Clone this repository:

```bash
git clone https://github.com/flathub/org.freedesktop.Platform.GL.nvidia.git
cd org.freedesktop.Platform.GL.nvidia
```

**4\.** Assuming you already know what driver version you want to build, use the following command to modify `versions.sh`:

```bash
# In this example, only the 560.35.03 driver will be built.
# You can also build multiple versions by separating them with a space.
echo 'DRIVER_VERSIONS="560.35.03"' >> versions.sh
```

**5\.** Invoke the build command to build for your CPU architecture:

```bash
make FB_ARGS='--user --install-deps-from=flathub'
```

**6\.** Create a local Flatpak remote named `nvidia-local`, pointing to the `repo/` directory:

```bash
flatpak --user remote-add --no-gpg-verify nvidia-local repo/
```

**7\.** Check what drivers you have in the repository:

```bash
flatpak --user remote-ls nvidia-local
```

**8\.** Install the drivers accordingly, for example:

```bash
flatpak --user install nvidia-local org.freedesktop.Platform.GL.nvidia-560-35-03
# And if you built the i386 driver...
flatpak --user install nvidia-local org.freedesktop.Platform.GL32.nvidia-560-35-03
```

**9\.** *(Optional)* If you want to free disk space, you can then disable the `nvidia-local` repository and delete the `repo` directory (this is safe, and will not uninstall your drivers):

```bash
flatpak --user remote-modify --disable nvidia-local
rm -rf repo/
```

To free even more disk space, you can also delete the `.flatpak-builder` and `builddir` directories (this is also safe):

```bash
rm -rf .flatpak-builder/ builddir/
```
