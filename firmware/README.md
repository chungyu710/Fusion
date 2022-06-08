## Installing the XC8 Compiler on Linux

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
