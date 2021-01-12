from datetime import date
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from lsp.lwm2m_object import Lwm2mObject
from lsp.util import split_array

import glob
import os
import time
import click
import multiprocessing

# zephyr-specific
TEMP_ZEPHYR_CMAKE = "zephyr_cmake.txt"
TEMP_ZEPHYR_KCONFIG = "zephyr_kconfig.txt"

# metadata
GEN_DATE = date.today().strftime("%m/%Y")


def get_template(templates_dir: str, template_name: str):
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    return template


def output_file(output: str, output_dir_path=None, output_file_name=None):
    """
    outputs a string either on console, if a target path is not provided, or to a file if its provided
    :param output: the data
    :param output_dir_path: path to the directory into which, the output will be written
    :param output_file_name: the name of the generated file
    """
    if output_dir_path is None:
        print(output)
    else:
        # make sure the directory exits
        path = Path(output_dir_path).absolute()
        if not Path.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            pass

        file_path = path / output_file_name
        source = open(file_path, "w")
        source.writelines(output)
        source.close()
        pass
    pass


def generate_hightlevel_lwm2m_object(templates_dir: str, template_name: str, xml_path: str,
                                     output_dir_path=None) -> Lwm2mObject:
    # TODO: first do xml Schema Validation?

    LWM2M_OBJ = Lwm2mObject(xml_path)
    LWM2M_OBJ.parse()

    template = get_template(templates_dir, template_name)
    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJ=LWM2M_OBJ)

    file_name = f"{LWM2M_OBJ.OBJ_NAME.lower()}_id{LWM2M_OBJ.OBJ_ID}.h"
    output_file(output, output_dir_path, file_name)

    print(f"generated high level representation of {xml_path}")
    return LWM2M_OBJ


def generate_lowlevel_lwm2m_source(templates_dir, template_name, lwm2m_obj: Lwm2mObject, output_dir_path=None):
    # import the template
    template = get_template(templates_dir, template_name)
    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJ=lwm2m_obj)

    file_name = f"{lwm2m_obj.OBJ_NAME.lower()}_id{lwm2m_obj.OBJ_ID}.c"
    output_file(output, output_dir_path, file_name)

    print(f"generated low level representation of {lwm2m_obj.xml_path}")
    return


def generate_zephyr_lwm2m_config(templates_dir, template_name, lwm2m_obj: [], output_dir_path=None,
                                 file_name: str = None):
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJECTS=lwm2m_obj)

    # check if we should output to file, or to console
    if output_dir_path is None:
        print(output)
    else:
        # make sure the directory exits
        path = Path(output_dir_path).absolute()
        if not Path.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            pass

        file = path / file_name
        zephyr_config = open(file, "w")
        zephyr_config.seek(0)
        zephyr_config.writelines(output)
        zephyr_config.truncate()
        zephyr_config.close()
        pass
    pass


# constants
TEMP_ZEPHYR_HIGHLEVEL = "lwm2m_object_template.txt"
TEMP_ZEPHYR_LOWLEVEL = "lwm2m_obj_zephyr_source.txt"
OUTPUT_HIGHLVL_DIR = "./generated/include/generated_lwm2m_objects/"
OUTPUT_LOWLVL_DIR = "./generated/subsys/lwm2m/generated/"
LWM2M_OBJ_REGISTRY = "https://github.com/OpenMobileAlliance/lwm2m-registry.git"
TEMPLATES_DIR = "./lsp/templates"
INPUT_DIR = "./xml"
FORCE_XML_UPDATE = False  # will force a clone of the latest XML files from github

generated_lwm2m_objects = []


def gen_code(xml_files, temp_dir, temp_highlvl, temp_lowlvl, output_highlvl, output_lowlvl):
    for xml_file in xml_files:
        print(f"parsing {xml_file}")
        lwm2m_object = generate_hightlevel_lwm2m_object(temp_dir, temp_highlvl, xml_file,
                                                        output_highlvl)
        generate_lowlevel_lwm2m_source(temp_dir, temp_lowlvl, lwm2m_object, output_lowlvl)
        generated_lwm2m_objects.append(lwm2m_object)
        print(f"finished parsing {lwm2m_object.xml_path} successfully!")
        print()
        pass
    pass


def generate(temp_dir, temp_highlvl, temp_lowlvl, output_highlvl, output_lowlvl, lwm2m_registry, force_update,
              input_dir, threads):
    ready = Path.exists(Path(input_dir)) and os.listdir(input_dir) != 0
    if not ready:
        print("input dir is empty or does not exist....exiting")
        exit(-1)
        pass

    if force_update:
        ready = os.system(f'git clone {lwm2m_registry} {input_dir}') == 0
        pass

    if not ready:
        print(
            "failed to retrieve XML Input files. make sure git is installed on your machine and added to "
            "PATH....existing")
        exit(-2)
        pass

    start_time = time.time()

    # get and loop over all XML files....
    lwm2m_xml_files = glob.glob(f"{INPUT_DIR}/*.xml")
    lwm2m_xml_files = list(filter(lambda x: Path(x).name.partition(".")[0].isnumeric(),
                                  lwm2m_xml_files))  # filter out none lwm2m objects, which are files that are not like this: <some number>.xml
    print(f"files to be parsed ({len(lwm2m_xml_files)} files): ", lwm2m_xml_files)
    if threads <= 1:
        gen_code(lwm2m_xml_files, temp_dir, temp_highlvl, temp_lowlvl, output_highlvl, output_lowlvl)
        pass
    else:
        split_xml = split_array(lwm2m_xml_files, threads)
        processes = []
        for i in range(threads):
            p = multiprocessing.Process(target=gen_code, args=(
            split_xml[i], temp_dir, temp_highlvl, temp_lowlvl, output_highlvl, output_lowlvl))
            p.start()
            processes.append(p)
            pass
        for p in processes:
            p.join()
        pass
    # ==========================================================================================

    # Zephyr specific
    print(f"successfully parsed {len(generated_lwm2m_objects)}, generating Kconfig and CmakeLists")
    # generate a Kconfig file to configure the usage of the generated code inside Zephyr Applications
    generate_zephyr_lwm2m_config(temp_dir, TEMP_ZEPHYR_KCONFIG, generated_lwm2m_objects,
                                 output_lowlvl, "Kconfig")
    # generate CMake to tie everything together
    generate_zephyr_lwm2m_config(temp_dir, TEMP_ZEPHYR_CMAKE, generated_lwm2m_objects,
                                 output_lowlvl, "CMakeLists.txt")
    print("finished generating Kconfig and CmakeLists. operation completed successfully")
    # =================================================================================================

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"execution time: {elapsed} seconds")
    pass


@click.command()
@click.option("--temp-dir", default=TEMPLATES_DIR,
              help="path to the directory containing the templates used to generate the code")
@click.option("--temp-highlvl", default=TEMP_ZEPHYR_HIGHLEVEL,
              help="name of the template that will be used to generate the high level code")
@click.option("--temp-lowlvl", default=TEMP_ZEPHYR_LOWLEVEL,
              help="name of the template that will be used to generate the high level code")
@click.option("--output-highlvl", default=OUTPUT_HIGHLVL_DIR, help="output directory of the generated high level code")
@click.option("--output-lowlvl", default=OUTPUT_LOWLVL_DIR, help="output directory of the generated low level code")
@click.option("--lwm2m-registry", default=LWM2M_OBJ_REGISTRY,
              help="URL to the Git Repository containing the XML files, depends on --force-update")
@click.option("--force-update", default=FORCE_XML_UPDATE, help="pulls the latest XML files from --lwm2m-registry",
              is_flag=True)
@click.option("--input-dir", default=INPUT_DIR, help="path to the directory containing the xml input files")
@click.option("--threads", default=4,
              help="number of threads created to run the parsing in parallel. default = 1 which means no multiprocessing")
def generate_cli(temp_dir, temp_highlvl, temp_lowlvl, output_highlvl, output_lowlvl, lwm2m_registry, force_update,
             input_dir, threads):

    generate(temp_dir, temp_highlvl, temp_lowlvl, output_highlvl, output_lowlvl, lwm2m_registry, force_update,
              input_dir, threads)
    pass


if __name__ == '__main__':
    # use Click
    generate_cli()

    # enable this to run code normally without using Click
    # generate(TEMPLATES_DIR, TEMP_ZEPHYR_HIGHLEVEL, TEMP_ZEPHYR_LOWLEVEL, OUTPUT_HIGHLVL_DIR, OUTPUT_LOWLVL_DIR,
    #          LWM2M_OBJ_REGISTRY, FORCE_XML_UPDATE, INPUT_DIR, multiprocessing.cpu_count())
    pass
