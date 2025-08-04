# To add a new driver

- Edit `versions.sh`, add new driver version.
- Run `update-data.sh`

The script will download the drivers from the nvidia servers and place the
 corresponding files in the `data` directory.

# Building locally

**1\.** Install the following packages:

```bash
flatpak git
```

**2\.** Add the Flathub repository:

```bash
flatpak --user remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

**3\.** Install `org.flatpak.Builder`:

```bash
flatpak --user install flathub org.flatpak.Builder
```

**4\.** Clone this repository:

```bash
git clone https://github.com/flathub/org.freedesktop.Platform.GL.nvidia.git
cd org.freedesktop.Platform.GL.nvidia
```

**5\.** Assuming you already know what driver version you want to build, use the following command to modify `versions.sh`:

```bash
# In this example, only the 560.35.03 driver will be built.
# You can also build multiple versions by separating them with a space.
echo 'DRIVER_VERSIONS="560.35.03"' >> versions.sh
```

**6\.** Run the `update-data.sh` script to ensure the required metadata files about the driver are present:

```bash
./update-data.sh
```

**7\.** Invoke the build command to build for your CPU architecture (Note: if you're on `x86_64`, the 32-bit driver also gets built):

```bash
flatpak run --command=make --env=FLATPAK_USER_DIR=$HOME/.local/share/flatpak org.flatpak.Builder
```

**8\.** Install the built drivers from the `./repo` directory:

```bash
flatpak --user install ./repo org.freedesktop.Platform.GL.nvidia-560-35-03
flatpak --user install ./repo org.freedesktop.Platform.GL32.nvidia-560-35-03 # 32-bit driver (if you built on x86_64)
```

**9\.** *(Optional)* To free disk space, you can delete the following directories (this is safe, and will not uninstall your drivers):

```bash
rm -rf .flatpak-builder/ builddir/ repo/
```
