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

5\. Install the appropriate 1.6 Freedesktop Platform/SDK for your CPU architecture:

```bash
flatpak --user install --no-related flathub "org.freedesktop.Platform/$(flatpak --default-arch)/1.6"
flatpak --user install --no-related flathub "org.freedesktop.Sdk/$(flatpak --default-arch)/1.6"
```

**6\.** This step is not mandatory, but highly recommended for `x86_64` users (`aarch64` users should skip this):

It's about building the `i386` driver, which is necessary for 32-bit 3D apps and games to work.

If you want to proceed, [these steps](https://github.com/guihkx/freedesktop-sdk-1.6-i386/releases/latest) will guide you on how to download and set up a third-party build (because it's not available on Flathub anymore) of the i386 1.6 Freedesktop SDK.

Once you finish doing that, you can continue following the steps below.

**7\.** Invoke the build command to build for your CPU architecture:

```bash
make FB_ARGS='--user'
```

**7. a)** *(Optional)* If you have set up the i386 1.6 SDK as suggested in the previous step, you also need to run these two commands to create a i386 build:

```bash
make ARCH=i386 FB_ARGS='--user'
flatpak build-update-repo --no-summary-index repo/
```

**8\.** Create a local Flatpak remote named `nvidia-local`, pointing to the `repo/` directory:

```bash
flatpak --user remote-add --no-gpg-verify nvidia-local repo/
```

**9\.** Check what drivers you have in the repository:

```bash
flatpak --user remote-ls nvidia-local
```

**10\.** Install the drivers accordingly, for example:

```bash
flatpak --user install nvidia-local org.freedesktop.Platform.GL.nvidia-560-35-03
# And if you built the i386 driver...
flatpak --user install nvidia-local org.freedesktop.Platform.GL32.nvidia-560-35-03
```

**11\.** *(Optional)* If you want to free disk space, you can then disable the `nvidia-local` repository and delete the `repo` directory (this is safe, and will not uninstall your drivers):

```bash
flatpak --user remote-modify --disable nvidia-local
rm -rf repo/
```

To free even more disk space, you can also delete the `.flatpak-builder` and `builddir` directories (this is also safe):

```bash
rm -rf .flatpak-builder/ builddir/
```
