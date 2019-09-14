# pip install --upgrade wmi
# pip install --upgrade pypiwin32

import wmi

computer = wmi.WMI()

computer_info = computer.Win32_ComputerSystem()[0]
os = computer.Win32_OperatingSystem()[0]
processor = computer.Win32_Processor()
gpu = computer.Win32_VideoController()


os_version = " ".join([os.Version, os.BuildNumber])
print(f"OS Version: {os_version}")

os_name = os.Name.split("|")[0]
print(f"OS Name: {os_name}")
print(f"Computer name: {computer_info.name}")
print(f"Username: {computer_info.username}")
print(f"Workgroup: {computer_info.workgroup}")
print(f"Domain: {computer_info.domain}")

print(f"CPU: {[cpu.name.strip() for cpu in processor]}")

system_ram = round(float(os.TotalVisibleMemorySize) / (1024 * 1024))  # KB to GB
print(f"RAM: {system_ram} GB")

print(f"Graphics Cards: {[g.name for g in gpu]}")

disks = computer.Win32_LogicalDisk()
print(f"Disks: {[disk.name for disk in disks]}")
