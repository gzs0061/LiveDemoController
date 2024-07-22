import SS_sim_controller_api as ss_api
import tkinter as tk
from functools import partial

'''
List of Buttons
Button Grouping

controller for live demo
	tag buttons
		4 states for entrance gate
			changes location of tag button obj
		ev plug in
			moves location out then back in
		dispatch
			moves location out then back in
	sim bus
		set sim target to entrance gate
		set sim target to ev turnaround
		set sim target to ev charger bay
		set sim target to dispatch bay 4
		set sim target to maint bay
		set sim target to outside maint bay
		set sim target to wash bay
		set sim target to outside wash bay
		
		teleport to entrance gate
			set sim target to null
			then set location to entrance gate
			set sim target to entrance gate
'''

# used to create a group of buttons, for diff simulation scenario groups' controls
def create_button_frame(root, frame_row, frame_col, group_name, buttons):
	# create a new frame to encapsulate the simu scenario controls
	frm_new = tk.Frame(master=root, borderwidth=2)

	# create a label for the sim scenario controls
	lbl_frame_header = tk.Label(master=frm_new, text=group_name, bg='grey', fg='white')
	lbl_frame_header.pack()

	# create all necessary control buttons
	for button in buttons:
		if button[1] != None:
			# wrap api function call with anonymous function to allow for arguments to be passed in
			# lambda : button[1](*button[2])
			# ^ this worked at first, but for some reason stopped working
			# imported partial function does essentially the same thing
			btn_new = tk.Button(master=frm_new, text=button[0], command= partial(button[1], *button[2]), borderwidth=2)
		else: # for testing purposes, creates null_functionality buttons when "None" command arg passed in
			btn_new = tk.Button(master=frm_new, text=button[0], borderwidth=2)
		btn_new.pack()

	# add the frame into the parent window at specified row and col in overall grid
	frm_new.grid(row=frame_row, column=frame_col)


def set_ip_from_entry(frame, entry):
	entry_text = entry.get()
	ss_api.set_ip(entry_text)
	label = tk.Label(frame, text="IP Address set to " + entry_text)
	label.pack()


# parent/main window init
root = tk.Tk()
root.title('Ubisense Transit') #SS DEMO SIM CONTROLLER')

'''
Create IP Input Form
'''
# create entry form for SS Instance IP address
ip_entry_frame = tk.Frame(master=root, borderwidth=2)
ip_entry_label = tk.Label(ip_entry_frame, text="Enter SmartSpace Public IP\nDefault IP : " + ss_api.smsp_ip_addr[0], bg='grey', fg='white')
ip_entry_label.pack()
entry = tk.Entry(ip_entry_frame, width=25)
entry.pack()
ip_partial_function_call=(set_ip_from_entry, [ip_entry_frame, entry])
ip_set_button = tk.Button(ip_entry_frame, text="Set IP", command=partial(ip_partial_function_call[0], *ip_partial_function_call[1]))
ip_set_button.pack()
ip_entry_frame.grid(row=0, column=0)

'''
variables for live depot control
'''
bus291_object_type = "Electric Bus"
bus291_object_name = "291"
bus125_object_type = "Fuel Bus"
bus125_object_name = "125"
bus_125_fuel_button = "_needs_fuel"
bus_125_fuel_true = "true"

tag_button_type = "Tag Button"
tag_button_entrance_gate = "North~20Depot~20Entrance~20Gate~20Button"
tag_button_ev_plug_in = "North~20Depot~20EV~20Plug~20In~20Button"
tag_button_dispatch = "North~20Depot~20Dispatch~20Button"

tag_button_offsite_loc_x = 705.7
tag_button_offsite_loc_y = 276.6
tag_button_offsite_loc_z = 1

tag_button_entrance_gate_dispatch_loc_x = 773.595
tag_button_entrance_gate_dispatch_loc_y = 273.611
tag_button_entrance_gate_dispatch_loc_z = 1

tag_button_entrance_gate_fuel_loc_x = 783.99
tag_button_entrance_gate_fuel_loc_y = 271.742
tag_button_entrance_gate_fuel_loc_z = 1

tag_button_entrance_gate_maint_loc_x = 792.579
tag_button_entrance_gate_maint_loc_y = 271.967
tag_button_entrance_gate_maint_loc_z = 1

tag_button_ev_plug_in_loc_x = 603.421
tag_button_ev_plug_in_loc_y = 125.482
tag_button_ev_plug_in_loc_z = 1

tag_button_dispatch_loc_x = 665.115
tag_button_dispatch_loc_y = 186.125
tag_button_dispatch_loc_z = 1

sim_target_type_button = "Tag Button"
sim_target_entrance_gate = "North Depot Sim Target Entrance Gate"
sim_target_ev_turnaround = "North Depot Sim Target EV Turnaround"
sim_target_outside_maint = "North Depot Sim Target Outside Maint"
sim_target_outside_wash = "North Depot Sim Target Outside Wash"
sim_target_outside_fuel = "North Depot Sim Target Outside Fuel"

sim_target_type_bay = "Parking Bay"
sim_target_ev_charger_bay = "North Depot EV Charger Bay"
sim_target_fuel_bay = "North Depot Fuel Bay"
sim_target_maint_bay = "North Depot Maintenance Bay"
sim_target_wash_bay = "North Depot Wash Bay"
sim_target_dispatch_4_bay = "North Depot Dispatch Bay"
sim_target_storage_bay = "North Depot Storage Bay"

entrance_gate_loc_x = 754.533
entrance_gate_loc_y = 285.144
entrance_gate_loc_z = 0.94


'''
- Entrance Gate Tag Buttons
'''
buttons = [('Entrance Gate Storage', ss_api.set_object_location, [tag_button_type, tag_button_entrance_gate, tag_button_offsite_loc_x, tag_button_offsite_loc_y, tag_button_offsite_loc_z, 0]),
			('Entrance Gate Dispatch', ss_api.set_object_location, [tag_button_type, tag_button_entrance_gate, tag_button_entrance_gate_dispatch_loc_x, tag_button_entrance_gate_dispatch_loc_y, tag_button_entrance_gate_dispatch_loc_z, 0]),
			('Entrance Gate Fuel', ss_api.set_object_location, [tag_button_type, tag_button_entrance_gate, tag_button_entrance_gate_fuel_loc_x, tag_button_entrance_gate_fuel_loc_y, tag_button_entrance_gate_fuel_loc_z, 0]),
			('Entrance Gate Maint', ss_api.set_object_location, [tag_button_type, tag_button_entrance_gate, tag_button_entrance_gate_maint_loc_x, tag_button_entrance_gate_maint_loc_y, tag_button_entrance_gate_maint_loc_z, 0])]
create_button_frame(root, 1, 0, 'Entrance Gate Tag Button', buttons)

'''
- EV Plug In Tag Button
'''
buttons = [('EV Plug In', ss_api.tag_button_out_in, [tag_button_type, tag_button_ev_plug_in, tag_button_offsite_loc_x, tag_button_offsite_loc_y, tag_button_offsite_loc_z, tag_button_ev_plug_in_loc_x, tag_button_ev_plug_in_loc_y, tag_button_ev_plug_in_loc_z, 0])]
create_button_frame(root, 1, 1, 'EV Plug In Tag Button', buttons)

'''
- Dispatch Tag Button
'''
buttons = [('Dispatch', ss_api.tag_button_out_in, [tag_button_type, tag_button_dispatch, tag_button_offsite_loc_x, tag_button_offsite_loc_y, tag_button_offsite_loc_z, tag_button_dispatch_loc_x, tag_button_dispatch_loc_y, tag_button_dispatch_loc_z, 0])]
create_button_frame(root, 1, 2, 'Dispatch Tag Button', buttons)


'''
- Bus 291 Movement
'''
buttons = [('Entrance Gate', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_button + "/" + sim_target_entrance_gate]),
			('EV Turnaround', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_button + "/" + sim_target_ev_turnaround]),
			('EV Charger Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_ev_charger_bay]),
			('Maint Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_maint_bay]),
			('Outside Maint Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_button + "/" + sim_target_outside_maint]),
			('Wash Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_wash_bay]),
			('Outside Wash Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_button + "/" + sim_target_outside_wash]),
			('Dispatch Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_dispatch_4_bay]),
			('Parking Bay', ss_api.set_object_property, [bus291_object_type, bus291_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_storage_bay])]

create_button_frame(root, 2, 0, 'Bus 291', buttons)

'''
- Bus 291 Reset
'''
buttons = [('Entrance Gate Reset', ss_api.reset_obj_to_loc, [bus291_object_type, bus291_object_name, entrance_gate_loc_x, entrance_gate_loc_y, entrance_gate_loc_z, -1.5707963267948966, sim_target_type_button + "/" + sim_target_entrance_gate])]
create_button_frame(root, 2, 1, 'Bus 291 Reset', buttons)

'''
- Bus 125 Movement
'''
buttons = [('EV Charger Bay', ss_api.set_object_property, [bus125_object_type, bus125_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_ev_charger_bay]),
			('Fuel Bay', ss_api.set_object_property, [bus125_object_type, bus125_object_name, 'simulation_target', sim_target_type_bay + "/" + sim_target_fuel_bay]),
			('Outside Fuel Bay', ss_api.set_object_property, [bus125_object_type, bus125_object_name, 'simulation_target', sim_target_type_button + "/" + sim_target_outside_fuel]),
			('Needs Fuel', ss_api.set_object_property, [bus125_object_type, bus125_object_name, bus_125_fuel_button, bus_125_fuel_true])]
create_button_frame(root, 2, 2, 'Bus 125', buttons)


root.mainloop()
