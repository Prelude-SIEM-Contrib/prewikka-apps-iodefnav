## IODEF nav plugins

This plugin add pretty UML graph of the IODEF schema. See [RFC
4765](https://www.ietf.org/rfc/rfc4765.txt).

It use graphviz to generate the graphs.

## How to use Prewikka apps

### Requirements

You need Prewikka 4.0.0 or higher.

### Source

The git repo for Prewikka apps is available on
[GitHub](https://github.com/Prelude-SIEM-Contrib/prewikka-apps-iodefnav) and
can be cloned like this:

    git clone https://github.com/Prelude-SIEM-Contrib/prewikka-apps-iodefnav.git

### Install

Once the source code downloaded:

    python setup.py install

Then edit /etc/prewikka/menu.yml and change the "question" menu to this :

- icon: question
  default: true
  categories:
      - sections:
            - name: Apps
              tabs:
                  - Apps
            - name: Help
              tabs:
                  - IODEF

Then restart Prewikka.

### License

The code is released under the GPLv2 license. See the COPYING file.

### Development

Please feel free to propose your own Prewikka plugins by submitting a pull
request.

## Specific

If you want to regenerate the graph with graphviz :

    python iodefnav/graph_generator.py
