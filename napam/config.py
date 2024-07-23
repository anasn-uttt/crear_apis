import napalm
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader
import yaml

def main():
    driver_ios = napalm.get_network_driver("ios")
    driver_vrp = napalm.get_network_driver("ce")

    device_list = [
        ["vrp-r2", "vrp", "router"],
        ["ios-r3", "ios", "router"]
    ]

    network_devices = []

    for device in device_list:
        if device[1] == "ios":
            network_devices.append(
                driver_ios(
                    hostname=device[0],
                    username="codingnetworks",
                    password="Coding.Networks1"
                )
            )
        elif device[1] == "vrp":
            network_devices.append(
                driver_vrp(
                    hostname=device[0],
                    username="codingnetworks",
                    password="Coding.Networks1"
                )
            )

    devices_table = [["hostname", "vendor", "model", "uptime", "serial_number"]]

    for device in network_devices:
        print("Connecting to {} ...".format(device.hostname))
        device.open()
        print("Getting device facts")
        device_facts = device.get_facts()
        devices_table.append([
            device_facts["hostname"],
            device_facts["vendor"],
            device_facts["model"],
            device_facts["uptime"],
            device_facts["serial_number"]
        ])
        # Cargar configuración desde plantilla
        device.load_merge_candidate(config=get_template_config(device_facts["vendor"]))
        print("\nDiff:")
        print(device.compare_config())
        # Confirmar o descartar cambios
        try:
            choice = input("\nWould you like to commit these changes? [yN]: ")
        except NameError:
            choice = input("\nWould you like to commit these changes? [yN]: ")
        if choice.lower() == 'y':
            print("Committing ...")
            device.commit_config()
        else:
            print("Discarding ...")
            device.discard_config()
        device.close()
        print("Done.")
    print(tabulate(devices_table, headers="firstrow"))

def get_template_config(vendor):
    config_data = yaml.load(open('{}_template.yml'.format(vendor)), Loader=yaml.FullLoader)
    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('{}_template.j2'.format(vendor))
    return template.render(config_data)

if __name__ == '__main__':
    main()
