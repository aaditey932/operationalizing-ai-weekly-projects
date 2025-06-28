import pandas as pd
from typing import  Literal, Optional
from langchain_core.tools import tool
from data_models.models import *
from datetime import datetime

@tool
def check_availability_by_doctor(desired_date:DateModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Checking the database if we have availability for the specific doctor.
    The parameters should be mentioned by the user in the query
    """
    #print("🔥 check_availability_by_doctor tool invoked with:")
    #print(f"desired_date: {desired_date},{type(desired_date)}")
    #print(f"doctor_name: {doctor_name} \n\n")
    
    try:

        df = pd.read_csv("data/doctor_availability.csv")

        #print(df,"\n\n")
        
        df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
        
        #print(df['date_slot_time'],"\n\n")

        rows = list(df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date)&(df['doctor_name'] == doctor_name)&(df['is_available'] == True)]['date_slot_time'])
        
        #print(rows,"\n\n")

        if len(rows) == 0:
            output = "No availability in the entire day"
        else:
            output = f'This availability for {desired_date.date}\n'
            output += "Available slots: " + ', '.join(rows)

        #print(output)

        return output
    
    except Exception as e:
        print("❌ Exception occurred in check_availability_by_doctor:", e)
        return f"An error occurred while checking availability: {str(e)}"
    
@tool
def check_availability_by_specialization(desired_date:DateModel, specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    """
    Checking the database if we have availability for the specific specialization.
    The parameters should be mentioned by the user in the query
    """
    #Dummy data
    #print("🔥 check_availability_by_specialization tool invoked with:")
    #print(f"desired_date: {desired_date},{type(desired_date)}")
    #print(f"specialization: {specialization} \n\n")

    try:

        df = pd.read_csv("data/doctor_availability.csv")
        df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
        rows = df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date) & (df['specialization'] == specialization) & (df['is_available'] == True)].groupby(['specialization', 'doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_slots')

        if len(rows) == 0:
            output = "No availability in the entire day"
        else:
            def convert_to_am_pm(time_str):
                # Split the time string into hours and minutes
                time_str = str(time_str)
                hours, minutes = map(int, time_str.split(":"))
                
                # Determine AM or PM
                period = "AM" if hours < 12 else "PM"
                
                # Convert hours to 12-hour format
                hours = hours % 12 or 12
                
                # Format the output
                return f"{hours}:{minutes:02d} {period}"
            output = f'This availability for {desired_date.date}\n'
            for row in rows.values:
                output += row[1] + ". Available slots: \n" + ', \n'.join([convert_to_am_pm(value)for value in row[2]])+'\n'

        return output

    except Exception as e:
        print("❌ Exception occurred in check_availability_by_doctor:", e)
        return f"An error occurred while checking availability: {str(e)}"
    
@tool
def set_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Set appointment or slot with the doctor.
    The parameters MUST be mentioned by the user in the query.
    """
    print("🔥 set_appointment tool invoked with:")
    print(f"desired_date_time: {desired_date},{type(desired_date)}")
    print(f"id_number: {id_number.id}, {type(id_number.id)}")
    print(f"doctor_name: {doctor_name} \n\n")

    try:
        patient_id = getattr(id_number, "id", id_number)
        
        df = pd.read_csv("data/doctor_availability.csv")

        case = df[
            (df['date_slot'] == desired_date.date) &
            (df['doctor_name'] == doctor_name) &
            (df['is_available'] == True)
            ]
        
        print("PATIENT ID --> ", patient_id)
        print(case,"\n\n")

        if len(case) == 0:
            print("No available appointments for that particular case")
            return "No available appointments for that particular case"
        else:
            
            df.loc[
                (df['date_slot'] == desired_date.date) &
                (df['doctor_name'] == doctor_name) & 
                (df['is_available'] == True), 
                ['is_available','patient_to_attend']] = [False, (patient_id)]
            
            df.to_csv("data/doctor_availability.csv", index = False)
            print("Successfully done")
            return "Successfully done"
        
    except Exception as e:
        print("❌ Exception occurred in set_appointment:", e)
        return f"An error occurred while setting appointment: {str(e)}"

@tool
def cancel_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Optional[Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']]):
    """
    Canceling an appointment.
    If doctor name is not provided, try to infer from patient ID and date.
    The parameters MUST be mentioned by the user in the query.
    """
    print("🔥 cancel_appointment tool invoked with:")
    print(f"desired_date_time: {desired_date},{type(desired_date)}")
    print(f"id_number: {id_number.id}, {type(id_number.id)}")
    print(f"doctor_name: {doctor_name} \n\n")

    try:
        patient_id = getattr(id_number, "id", id_number)
        print("PATIENT ID --> ", patient_id)

        df = pd.read_csv("data/doctor_availability.csv")

        if doctor_name:
            case_to_remove = df[
                (df['date_slot'] == desired_date.date) &
                (df['patient_to_attend'] == patient_id) &
                (df['doctor_name'] == doctor_name)
                ]
        else:
            case_to_remove = df[
                (df['date_slot'] == desired_date.date) &
                (df['patient_to_attend'] == patient_id)
                ]
        
        if len(case_to_remove) == 0:
            return "You don´t have any appointment with that specifications"
        
        elif len(case_to_remove) == 1:
            matched_row = case_to_remove.iloc[0]
            df.loc[
                (df['date_slot'] == matched_row['date_slot']) &
                (df['patient_to_attend'] == patient_id) & 
                (df['doctor_name'] == matched_row['doctor_name']), 
                ['is_available', 'patient_to_attend']] = [True, None]
            df.to_csv("data/doctor_availability.csv", index = False)
            return f"Your appointment with Dr. {matched_row['doctor_name'].title()} at {matched_row['date_slot']} has been cancelled."

        else:
            # Multiple matches — need user confirmation
            options = "\n".join(
                f"- Dr. {row['doctor_name'].title()} at {row['date_slot']}"
                for _, row in case_to_remove.iterrows()
            )
            return f"You have multiple appointments on that day:\n{options}\nPlease specify which one to cancel."

        
    except Exception as e:
        print("❌ Exception occurred in cancel_appointment:", e)
        return f"An error occurred while cancelling appointment: {str(e)}"
@tool
def reschedule_appointment(old_date:DateTimeModel, new_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    """
    Rescheduling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    print("🔥 reschedule_appointment tool invoked with:")
    print(f"old_date: {old_date},{type(old_date)}")
    print(f"new_date: {new_date},{type(new_date)}")
    print(f"id_number: {id_number.id}, {type(id_number.id)}")
    print(f"doctor_name: {doctor_name} \n\n")

    try:
        patient_id = getattr(id_number, "id", id_number)
        print("PATEINT ID TYPE ++> ", type(patient_id))
        df = pd.read_csv("data/doctor_availability.csv")

        available_for_desired_date = df[
            (df['date_slot'] == new_date.date) &
            (df['is_available'] == True) &
            (df['doctor_name'] == doctor_name)
            ]
        
        if len(available_for_desired_date) == 0:
            return "Not available slots in the desired period"
        else:
            cancel_appointment.invoke({'desired_date':old_date, 'id_number':id_number, 'doctor_name':doctor_name})
            set_appointment.invoke({'desired_date':new_date, 'id_number': id_number, 'doctor_name': doctor_name})
            return "Successfully rescheduled for the desired time"
    
    except Exception as e:
        print("❌ Exception occurred in reschedule_appointment:", e)
        return f"An error occurred while rescheduling: {str(e)}"