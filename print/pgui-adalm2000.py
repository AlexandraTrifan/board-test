
import Tkinter
import pyudev
import subprocess

def adalm_status_update(device):
	if device.action == "add":
		adalm_status_string.set("Connected")
		adalm_status.config(fg="Green")
		window.update_idletasks()
	elif device.action == "remove":
		adalm_status_string.set("Disconnected")
		adalm_status.config(fg="Red")
		window.update_idletasks()

def print_callback_adalm():
        dymo_jobs_string.set("Printing, wait...")
        dymo_jobs.config(fg="Black")
        window.update_idletasks()
        do = subprocess.Popen("./print_m2k_back.sh", stdout=subprocess.PIPE, shell=True)
        (output, err) = do.communicate()
        do_status = do.wait()
        if do_status == 1:
                dymo_jobs_string.set("Printing Failed")
                dymo_jobs.config(fg="Red")
        else:
                dymo_jobs_string.set("Printing Done")
                dymo_jobs.config(fg="Green")
        print "Command output : ", output
        print "Command exit status/return code : ", do_status


def shutdown_callback():
        do = subprocess.Popen("sudo shutdown -h now", stdout=subprocess.PIPE, shell=True)

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

observer = pyudev.MonitorObserver(monitor, callback=adalm_status_update)
observer.daemon
observer.start()

window = Tkinter.Tk()
window.title("ADALM2000 Label")
window.attributes("-fullscreen", True)

adalm_label = Tkinter.Label(window, text ="ADALM2000", font=("Courier", 30, "bold"))
adalm_label.grid(row=0, column=0)
adalm_status_label = Tkinter.Label(window, text ="status:", font=("Courier", 30))
adalm_status_label.grid(row=1, column=0)
adalm_status_string = Tkinter.StringVar(window, value="Disconnected")
adalm_status = Tkinter.Label(window, textvariable = adalm_status_string, font=("Courier", 30))
adalm_status.config(fg="Red")
adalm_status.grid(row=1, column=1)

dymo_label = Tkinter.Label(window, text ="DYMO Printer", font=("Courier", 30, "bold"))
dymo_label.grid(row=10, column=0)
dymo_status_label = Tkinter.Label(window, text ="status:", font=("Courier", 30))
dymo_status_label.grid(row=11, column=0)
dymo_install = subprocess.Popen("python ./dymo_install.py", stdout=subprocess.PIPE, shell=True)
(output, err) = dymo_install.communicate()
dymo_install_status = dymo_install.wait()
if dymo_install_status != 0:
	dymo_status = Tkinter.Label(window, text = "Not Installed", font=("Courier", 30))
	dymo_status.config(fg="Red")
else:
	dymo_status = Tkinter.Label(window, text = "Available", font=("Courier", 30))
	dymo_status.config(fg="Green")
dymo_status.grid(row=11, column=1)
dymo_jobs_label = Tkinter.Label(window, text ="jobs:", font=("Courier", 30))
dymo_jobs_label.grid(row=12, column=0)
dymo_jobs_string = Tkinter.StringVar(window, value="Idle")
dymo_jobs = Tkinter.Label(window, textvariable = dymo_jobs_string, font=("Courier", 30))
dymo_jobs.grid(row=12, column=1)

adalm_print_button = Tkinter.Button(window, text="Print Label ADALM2000", font=("Courier", 30), command = print_callback_adalm)
adalm_print_button.grid(row=13, column=0)

util_label = Tkinter.Label(window, text ="Util", font=("Courier", 30, "bold"))
util_label.grid(row=20, column=0)
shutdown_button = Tkinter.Button(window, text = "Shutdown", font=("Courier", 30), command = shutdown_callback)
shutdown_button.grid(row=21, column=0)
quit_button = Tkinter.Button(window, text = "Quit", font=("Courier", 30), command = window.destroy)
quit_button.grid(row=22, column=0)

window.mainloop()
