# Graph Isomorphism and Counting Automorphisms
## Group 13
### Required files
* main.py
* graph.py (our version)
* graph_io.py (our version)
* individualization.py
* refined_colouring.py
* automorphismGenerator.py
* permv2.py
* basicpermutationgroup.py


### Usage guide
Running ``main.py`` can be done with several **required** arguments:
* ``-i or --input_file=`` - specifies the name of the file with the extension eg. "torus24.grl" or "threepaths80.gr" (this requires that the files must have ``.gr or .grl`` extensions)
* ```-g or --graph_iso=``` - set to 1 if you want to run the graph isomorphism test and 0 if not
* ``-c or --count_auto=`` - set to 1 if you want to count the number of automorphisms and 0 if not

This example: ```python3 main.py -i torus24.grl -c 1``` will compute the number of automorphism for the graphs found in the provided file.

One can also run ```main.py -h``` for a reminder of this usage.

**Important!**
Please make sure to add the graph files (``.gr or .grl``) in a folder called ``graphs``.

### Authors:
* Eduard Constantinescu - s1922629
* Marieke Romeijn - s1992988
* Catalin Rus - s1910426 
* Andrei Popa - s1957058