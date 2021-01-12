# LwM2M Source Parser (LSP)
A python tool that parsers XML documents describing LwM2M Objects, 
and generates source code (by default a C source file and a C++ Header file), 
tailored to be applied in a Zephyr-RTOS environment for lwm2m client applications.

this package can be forked and easily adjusted to apply the parsed data to other development
environments, not just Zephyr

# dependencies
this package uses the template engine Jinja2 so this will need to be installed:

    pip3 install jinja2

this package supports pulling the latest [XML OMA registry](https://github.com/OpenMobileAlliance/lwm2m-registry.git) from GitHub,
in this case, git will need to already be installed and added to PATH on your machine.

