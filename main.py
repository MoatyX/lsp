from datetime import date
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from lwm2m_object import Lwm2mObject

import glob
import os
import time
import multiprocessing

GENERATED_LWM2M_INCLUDE_OUTPUT_DIR = "./generated/include/generated_lwm2m_objects/"
GENERATED_ZEPHYR_OUTPUT_DIR = "./generated/subsys/lwm2m/generated/"
TEMP_ZEPHYR_SOURCE = "lwm2m_obj_zephyr_source.txt"
TEMP_ZEPHYR_CMAKE = "zephyr_cmake.txt"
TEMP_ZEPHYR_KCONFIG = "zephyr_kconfig.txt"
LWM2M_OBJ_REGISTRY = "https://github.com/OpenMobileAlliance/lwm2m-registry.git"
TEMPLATES_DIR = "./templates"
TEMP_LWM2M_OBJECTS = "lwm2m_object_template.txt"
INPUT_DIR = "./xml"

# metadata
GEN_DATE = date.today().strftime("%m/%Y")


def generate_lwm2m_object(templates_dir: str, template_name: str, xml_path: str, output_dir_path=None) -> Lwm2mObject:
    # TODO: first do xml Schema Validation

    LWM2M_OBJ = Lwm2mObject(xml_path)
    LWM2M_OBJ.parse()

    # import the template
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)

    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJ=LWM2M_OBJ)

    # check if we should output to file, or to console
    if output_dir_path is None:
        print(output)
    else:
        # make sure the directory exits
        path = Path(output_dir_path).absolute()
        if not Path.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            pass

        cpp_header_file_path = path / f"{LWM2M_OBJ.OBJ_NAME.lower()}_id{LWM2M_OBJ.OBJ_ID}.h"
        cpp_header = open(cpp_header_file_path, "w")
        cpp_header.writelines(output)
        cpp_header.close()
        pass

    print(f"generated C++ include for {xml_path}")
    return LWM2M_OBJ


def generate_zephyr_source_obj(templates_dir, template_name, lwm2m_obj: Lwm2mObject, output_dir_path=None):
    # import the template
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJ=lwm2m_obj)

    # check if we should output to file, or to console
    if output_dir_path is None:
        print(output)
    else:
        # make sure the directory exits
        path = Path(output_dir_path).absolute()
        if not Path.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            pass

        c_file_path = path / f"{lwm2m_obj.OBJ_NAME.lower()}_id{lwm2m_obj.OBJ_ID}.c"
        zephyr_c_source = open(c_file_path, "w")
        zephyr_c_source.writelines(output)
        zephyr_c_source.close()
        pass

    print(f"generated Zephyr Source Definition {lwm2m_obj.OBJ_NAME.lower()}_{lwm2m_obj.OBJ_ID}")
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


if __name__ == '__main__':
    force_update_xml_registry = False   # TODO: make this into CLI
    ready = Path.exists(Path(INPUT_DIR)) and os.listdir(INPUT_DIR) != 0
    update_xml_registry = not ready or force_update_xml_registry
    if update_xml_registry:
        ready = os.system(f'git clone {LWM2M_OBJ_REGISTRY} {INPUT_DIR}') == 0
        pass

    if not ready:
        print("failed to retrieve XML Input files. make sure git is installed on your machine and added to PATH")
        exit(-1)
        pass

    generated_lwm2m_objects = []

    start_time = time.time()

    # get and loop over all XML files....
    lwm2m_xml_files = glob.glob(f"{INPUT_DIR}/*.xml")
    lwm2m_xml_files = list(filter(lambda x: Path(x).name.partition(".")[0].isnumeric(), lwm2m_xml_files))       # filter out none lwm2m objects
    print(f"files to be parsed ({len(lwm2m_xml_files)} files): ", lwm2m_xml_files)
    for xm_file in lwm2m_xml_files:
        print(f"parsing {xm_file}")
        lwm2m_object = generate_lwm2m_object(TEMPLATES_DIR, TEMP_LWM2M_OBJECTS, xm_file, GENERATED_LWM2M_INCLUDE_OUTPUT_DIR)
        generate_zephyr_source_obj(TEMPLATES_DIR, TEMP_ZEPHYR_SOURCE, lwm2m_object, GENERATED_ZEPHYR_OUTPUT_DIR)
        generated_lwm2m_objects.append(lwm2m_object)
        print(f"finished parsing {lwm2m_object.xml_path} successfully!")
        print()
        pass
    # end of the for loop

    print(f"successfully parsed {len(generated_lwm2m_objects)}, generating Kconfig and CmakeLists")
    # generate a Kconfig file to configure the usage of the generated code inside Zephyr Applications
    generate_zephyr_lwm2m_config(TEMPLATES_DIR, TEMP_ZEPHYR_KCONFIG, generated_lwm2m_objects,
                                 GENERATED_ZEPHYR_OUTPUT_DIR, "Kconfig")
    # generate CMake to tie everything together
    generate_zephyr_lwm2m_config(TEMPLATES_DIR, TEMP_ZEPHYR_CMAKE, generated_lwm2m_objects,
                                 GENERATED_ZEPHYR_OUTPUT_DIR, "CMakeLists.txt")
    print("finished generating Kconfig and CmakeLists. operation completed successfully")

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"execution time: {elapsed} seconds")
    pass
