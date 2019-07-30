#### How to install

###### Symlink

```
  git clone https://github.com/linux-genz/genz_xml_parser.git
  sudo ln -s $PWD/genz_xml_parser/gxp /usr/lib/python3/dist-packages/gxp
```

Or add a path to a genz_xml_parser/gxp to a PYTHONPATH environment variable.


###### Setup script

```
  TODO
  NOT YET IMPLEMENTED
```


#### HOW TO RUN

```
 ./xml_to_header.py -h
```


###### To use a local path

```
xml_to_header.py /path/to/file.xml -o destination_header.h
```

###### To use path as URL:
```
xml_to_header.py http://some_url/to/a/file.xml -o destination_header.h
```

###### NOTE: .h in the output file name is required! Otherwise - bada-boom.