# Firmware

The PIC16F690 microcontroller runs embedded C firmware to read sensor data and relay it to the host.  The C firmware must be cross-compiled using Microchip's XC8 compiler toolchain.

## Installing XC8 on Linux

Go to your home directory.
```
cd ~
```

Download the XC8 installer.
```
curl -L http://www.microchip.com/mplabxc8linux -o xc8-installer
```

Make the installer executable.
```
chmod u+x xc8-installer
```

Run the installer and make sure to select the free version.  Don't activate the license or the free trial.
```
sudo ./xc8-installer
```

Add the XC8 tools to your PATH environment variable.
```
echo 'export PATH="${PATH}:/opt/microchip/xc8/v2.36/bin/"' >> ~/.bashrc
echo 'export PATH="${PATH}:/opt/microchip/mplabx/v5.50/mplab_platform/mplab_ipe/bin"' >> ~/.bashrc
```

Reload your `.bashrc`.
```
source ~/.bashrc
```

Try running XC8.
```
xc8-cc
```

Delete the installer if everything went well.
```
rm xc8-installer
```

## Compiling Code

From the top-level directory (`firmware/`):
```
make
```

This will compile and link all source files under `firmware/`.  The output hex file should be found at `build/fusion.hex`.  You can flash this to the PIC using MPLAB IPE and a PICKit3 ICSP.

## Flashing the PIC

```
ipecmd.sh -TPPK3 -P16F690 -M -F"<absolute/path/to/fusion.hex>"
```

The path to the hex file must not contain spaces, e.g.:
```
ipecmd.sh -TPPK3 -P16F690 -M -F"/Users/Kyle/capstone/firmware/build/fusion.hex"
```

## Pairing Bluetooth Modules

Use `miniterm.py` that came with pyserial.

## USB-TTL Converter

Install the CP210x drivers
https://www.silabs.com/interface/usb-bridges/classic/device.cp2102
