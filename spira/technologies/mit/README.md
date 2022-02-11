
**Download** the SPiRA framework: https://github.com/rubenvanstaden/spira
**Documentation** can be found at: https://spira.readthedocs.io/en/latest/

Copy this ``mit`` folder into the ``technologies`` folder in SPiRA's root directory.
For example: ``/home/therealtyler/code/spira/technologies``. Your technologies tree
should then look something like this:

```
technologies
|__ default
|__ mit
    |__ devices
    |__ circuits
    |__ process
```

The ``default`` directory is a custom made fabrication process that is used as default
if no specific process is specified. To run an example make sure you are in the spira
root directory and then simply run:

```
python spira/technologies/mit/circuits/lieze_jtl.py
```



