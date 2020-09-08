# -*- coding: utf-8 -*-
# Test name = Software Upgrade
# Test description = Set environment, perform software upgrade and check STB after sw upgrade

from datetime import datetime
from time import gmtime, strftime
import time
import os.path
import sys
import device
import shutil
import TEST_CREATION_API

THRESHOLD = 60

WAIT_FOR_IMAGE = 100

try:    
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py")) == False) or (str(os.path.getmtime('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py')) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))))):
        shutil.copy2('\\\\rt-rk01\\RT-Executor\\API\\NOS_API.py', os.path.join(os.path.dirname(sys.executable), "Lib\NOS_API.py"))
except:
    pass

import NOS_API
    
try:
    # Get model
    model_type = NOS_API.get_model()

    # Check if folder with thresholds exists, if not create it
    if(os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds")) == False):
        os.makedirs(os.path.join(os.path.dirname(sys.executable), "Thresholds"))

    # Copy file with threshold if does not exists or if it is updated
    if ((os.path.exists(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt")) == False) or (str(os.path.getmtime(NOS_API.THRESHOLDS_PATH + model_type + ".txt")) != str(os.path.getmtime(os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))))):
        shutil.copy2(NOS_API.THRESHOLDS_PATH + model_type + ".txt", os.path.join(os.path.dirname(sys.executable), "Thresholds\\" + model_type + ".txt"))
except Exception as error_message:
    pass

## Number of alphanumeric characters in SN
SN_LENGTH = 14  

## Number of alphanumeric characters in Cas_Id
CASID_LENGTH = 12
    
def runTest():

    System_Failure = 0
    
    NOS_API.read_thresholds()
    
    NOS_API.reset_test_cases_results_info()
    
    #NOS_API.Remove_UMA_FIFO("22934")

    while (System_Failure < 2):
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"
            
            error_codes = ""
            error_messages = ""
            
            SN_LABEL = False
            CASID_LABEL = False
        
            ## Read STB Labels using barcode reader (S/N, CAS ID) and LOG it             
            all_scanned_barcodes = NOS_API.get_all_scanned_barcodes()
            
            if not(len(all_scanned_barcodes) == 3):
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                               + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message
                
                NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report_file = NOS_API.create_test_case_log_file(
                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                NOS_API.test_cases_results_info.nos_sap_number,
                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                "",
                                end_time)
                NOS_API.upload_file_report(report_file)
                NOS_API.test_cases_results_info.isTestOK = False

                ## Update test result
                TEST_CREATION_API.update_test_result(test_result)
                
                ## Return DUT to initial state and de-initialize grabber device
                NOS_API.deinitialize()
                
                NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)

                return
                
            NOS_API.test_cases_results_info.s_n_using_barcode = all_scanned_barcodes[1]
            NOS_API.test_cases_results_info.cas_id_using_barcode = all_scanned_barcodes[2]
            NOS_API.test_cases_results_info.nos_sap_number = all_scanned_barcodes[0]
            
            test_number = NOS_API.get_test_number(NOS_API.test_cases_results_info.s_n_using_barcode)
            device.updateUITestSlotInfo("Teste N\xb0: " + str(int(test_number)+1))
            
            if ((len(NOS_API.test_cases_results_info.s_n_using_barcode) == SN_LENGTH) and (NOS_API.test_cases_results_info.s_n_using_barcode.isalnum() or NOS_API.test_cases_results_info.s_n_using_barcode.isdigit())):
                SN_LABEL = True
            
            if ((len(NOS_API.test_cases_results_info.cas_id_using_barcode) == CASID_LENGTH) and (NOS_API.test_cases_results_info.cas_id_using_barcode.isalnum() or NOS_API.test_cases_results_info.cas_id_using_barcode.isdigit())):
                CASID_LABEL = True
            
            if not(SN_LABEL and CASID_LABEL):
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.scan_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.scan_error_message)
                NOS_API.set_error_message("Leitura de Etiquetas")
                error_codes = NOS_API.test_cases_results_info.scan_error_code
                error_messages = NOS_API.test_cases_results_info.scan_error_message
                
                NOS_API.add_test_case_result_to_file_report(
                                test_result,
                                "- - - - - - - - - - - - - - - - - - - -",
                                "- - - - - - - - - - - - - - - - - - - -",
                                error_codes,
                                error_messages)
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report_file = NOS_API.create_test_case_log_file(
                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                NOS_API.test_cases_results_info.nos_sap_number,
                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                "",
                                end_time)
                NOS_API.upload_file_report(report_file)
                NOS_API.test_cases_results_info.isTestOK = False

                ## Update test result
                TEST_CREATION_API.update_test_result(test_result)
                
                ## Return DUT to initial state and de-initialize grabber device
                NOS_API.deinitialize()
                
                NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)

                return

            if (NOS_API.configure_power_switch_by_inspection()):
                NOS_API.power_off() 
                time.sleep(2)
            else:
                TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                ## Update test result
                TEST_CREATION_API.update_test_result("FAIL")
                NOS_API.set_error_message("POWER SWITCH")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                error_codes = NOS_API.test_cases_results_info.power_switch_error_code
                error_messages = NOS_API.test_cases_results_info.power_switch_error_message
                ## Return DUT to initial state and de-initialize grabber device
                NOS_API.deinitialize()
                NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - - - - - - - - - - - - - - - - - - -",
                    "- - - - - - - - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
             
                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report_file = NOS_API.create_test_case_log_file(
                            NOS_API.test_cases_results_info.s_n_using_barcode,
                            NOS_API.test_cases_results_info.nos_sap_number,
                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                            NOS_API.test_cases_results_info.mac_using_barcode,
                            end_time)
                NOS_API.upload_file_report(report_file)
                
                NOS_API.send_report_over_mqtt_test_plan(
                    test_result,
                    end_time,
                    error_codes,
                    report_file)
             
                
                return
             
            ## Power switch on
            NOS_API.power_on()
            time.sleep(1)
            
            if (System_Failure == 0):
                if not(NOS_API.display_new_dialog("Conectores?", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"): 
                    TEST_CREATION_API.write_log_to_file("Conectores NOK")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.conector_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.conector_nok_error_message)  
                    NOS_API.set_error_message("Danos Externos")
                    error_codes = NOS_API.test_cases_results_info.conector_nok_error_code
                    error_messages = NOS_API.test_cases_results_info.conector_nok_error_message
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    "",
                                    end_time)
                    NOS_API.upload_file_report(report_file)
                    NOS_API.test_cases_results_info.isTestOK = False

                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)

                    return
                if not(NOS_API.display_custom_dialog("Inserir SmartCard! A STB est\xe1 ligada?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                    TEST_CREATION_API.write_log_to_file("No Power")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_power_error_code \
                                                                   + "; Error message: " + NOS_API.test_cases_results_info.no_power_error_message)
                    NOS_API.set_error_message("Não Liga")
                    error_codes = NOS_API.test_cases_results_info.no_power_error_code
                    error_messages = NOS_API.test_cases_results_info.no_power_error_message
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    report_file = NOS_API.create_test_case_log_file(
                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                    NOS_API.test_cases_results_info.nos_sap_number,
                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                    "",
                                    end_time)
                    NOS_API.upload_file_report(report_file)
                    NOS_API.test_cases_results_info.isTestOK = False

                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                            test_result,
                            end_time,
                            error_codes,
                            report_file)

                    return
                    
            NOS_API.Send_Serial_Key("a", "feito")
            time.sleep(1)
            
            NOS_API.grabber_hour_reboot()
            
            ## Initialize grabber device
            NOS_API.initialize_grabber()       
    
            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
        
            # Get start time
            start_time = time.localtime()
            delta_time = 0
            signal_detected_on_hdmi = False
            signal_detected_on_cvbs = False
            counter_ended = False
            sw_upgrade_detected = False
            Nagra_Upgrade = False
            while(counter_ended == False):
                if(delta_time > WAIT_FOR_IMAGE):
                    counter_ended = True
                    break
                    
                signal_detected_on_hdmi = False
                signal_detected_on_cvbs = False
                sw_upgrade_detected = False
                
                # Get current time and check is testing finished
                delta_time = (time.mktime(time.localtime()) - time.mktime(start_time))   


                if not(NOS_API.wait_for_signal_present(5)):
                    time.sleep(10)
                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    time.sleep(5)
            
                if (NOS_API.wait_for_signal_present(15)):
                    
                    result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_started_via_ota", "new_sw_detected_message_576", "new_sw_detected_message_720", "new_sw_detected_message_1080", "Check_Nagra_ref", "Check_Nagra_1080_ref"], 15, ["[WRITE_SW_HDMI]", "[SW_UPGRADE_MESSAGE_576]", "[SW_UPGRADE_MESSAGE_720]", "[SW_UPGRADE_MESSAGE_1080]", "[Nagra_Upgrade]", "[Nagra_Upgrade_1080]"], [80, 80, 80, 80, 80, 80])
                    
                    if (result == -2):
                        continue
                    
                    if (result != -1):
                        if(result == 4 or result == 5):
                            Nagra_Upgrade = True
                        sw_upgrade_detected = True
                        signal_detected_on_hdmi = True
                        signal_detected_on_cvbs = True
                        break
                    
                    TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                    TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                
                    result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_ref", "installation_boot_up_1080_ref", "menu_576_ref", "menu_720_ref", "menu_1080_ref", "menu_576_new_ref", "menu_720_new_ref", "menu_1080_new_ref", "new_sw_detected_message_576", "new_sw_detected_message_720", "new_sw_detected_message_1080"], 25, ["[INSTALLATION_BOOT_UP]", "[INSTALLATION_BOOT_UP_1080]", "[MENU_576]", "[MENU_720]", "[MENU_1080]", "[MENU_NEW_576]", "[MENU_NEW_720]", "[MENU_NEW_1080]", "[SW_UPGRADE_MESSAGE_576]", "[SW_UPGRADE_MESSAGE_720]", "[SW_UPGRADE_MESSAGE_1080]"], [80, 80, 70, 70, 70, 70,70,70, 80,80,80])
                    
                    if (result == 0 or result == 1):
                        NOS_API.test_cases_results_info.channel_boot_up_state = False
                        signal_detected_on_hdmi = True
                        signal_detected_on_cvbs = True
                        break
                    elif(result >= 2 and result <= 7):
                        NOS_API.test_cases_results_info.channel_boot_up_state = True
                        signal_detected_on_hdmi = True
                        signal_detected_on_cvbs = True
                        break
                    elif(result >= 8 and result <= 10):
                        sw_upgrade_detected = True
                        signal_detected_on_hdmi = True
                        signal_detected_on_cvbs = True
                        break
                    else:
                        ## Start grabber device with video on CVBS
                        NOS_API.grabber_stop_video_source()
                        NOS_API.reset_dut()
                        ##time.sleep(2)
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS)

                        TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                        TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                        
                        result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_cvbs_ref", "menu_cvbs", "new_sw_detected_message_cvbs"], 5, ["[INSTALLATION_BOOT_UP_CVBS]", "[MENU_CVBS]", "[SW_UPGRADE_MESSAGE_CVBS]"], [30, 30, 30])
                        if (result == -2):
                            NOS_API.grabber_stop_video_source()
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            continue
                        if(result != -1):
                            signal_detected_on_cvbs = True
                        else:
                            NOS_API.grabber_stop_video_source()
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            continue
                            
                        ## Start grabber device with video on HDMI1
                        NOS_API.grabber_stop_video_source()
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        
                        result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_started_via_ota", "new_sw_detected_message_576", "new_sw_detected_message_720", "new_sw_detected_message_1080", "Check_Nagra_ref", "Check_Nagra_1080_ref"], 15, ["[WRITE_SW_HDMI]", "[SW_UPGRADE_MESSAGE_576]", "[SW_UPGRADE_MESSAGE_720]", "[SW_UPGRADE_MESSAGE_1080]", "[Nagra_Upgrade]", "[Nagra_Upgrade_1080]"], [80, 80, 80, 80, 80, 80])
                        
                        if (result == -2):
                            continue
                        if (result != -1):
                            if(result == 4 or result == 5):
                                Nagra_Upgrade = True
                            sw_upgrade_detected = True
                            signal_detected_on_hdmi = True
                        
                        TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                        TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                        result = NOS_API.wait_for_multiple_pictures(["installation_boot_up_ref", "installation_boot_up_1080_ref", "menu_576_ref", "menu_720_ref", "menu_1080_ref", "menu_576_new_ref", "menu_720_new_ref", "menu_1080_new_ref", "new_sw_detected_message_576", "new_sw_detected_message_720", "new_sw_detected_message_1080"], 25, ["[INSTALLATION_BOOT_UP]", "[INSTALLATION_BOOT_UP_1080]","[MENU_576]", "[MENU_720]", "[MENU_1080]", "[MENU_NEW_576]", "[MENU_NEW_720]", "[MENU_NEW_1080]", "[SW_UPGRADE_MESSAGE_576]", "[SW_UPGRADE_MESSAGE_720]", "[SW_UPGRADE_MESSAGE_1080]"], [80, 80, 70, 70, 70, 70,70,70, 80,80,80])
                        if (result == -2):
                            continue
                        if (result == 0 or result == 1):
                            NOS_API.test_cases_results_info.channel_boot_up_state = False
                            signal_detected_on_hdmi = True
                        elif(result >= 2 and result <= 7):
                            NOS_API.test_cases_results_info.channel_boot_up_state = True
                            signal_detected_on_hdmi = True
                        elif(result >= 8 and result <= 10):
                            signal_detected_on_hdmi = True
                            sw_upgrade_detected = True
                        if((signal_detected_on_hdmi == False) and (signal_detected_on_cvbs == True)):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
            
                            return
                
                        if((signal_detected_on_hdmi == True) and (signal_detected_on_cvbs == True)):
                            break            
                else:
                    ## Start grabber device with video on CVBS
                    NOS_API.grabber_stop_video_source()
                    NOS_API.reset_dut()
                    #time.sleep(2)
                    NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS)
                    #time.sleep(3)
                    
                    ## If there is signal on CVBS
                    if (NOS_API.wait_for_signal_present(5)):
                    
                        ## If black screen appears
                        result = NOS_API.wait_for_multiple_pictures(["black_screen_cvbs"], 5, ["[FULL_SCREEN_576_execpt_corner]"], [80])
                        if (result == -2):
                            NOS_API.grabber_stop_video_source()
                            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                            continue
                        if(result != -1):
                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            time.sleep(10)
                            
                            ## If black screen doesn't appear, HMDI NOK
                            result = NOS_API.wait_for_multiple_pictures(["black_screen_cvbs"], 2, ["[FULL_SCREEN_576_execpt_corner]"], [80])
                            if(result == -1):
                                if not (NOS_API.grab_picture("Scart_Image")):
                                    TEST_CREATION_API.write_log_to_file("No video SCART.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                                    NOS_API.set_error_message("Video Scart")
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                    
                                    return
                                
                                NOS_API.grabber_stop_video_source()
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                if(NOS_API.is_signal_present_on_video_source()):
                                    continue
                                else:
                                    NOS_API.display_dialog("Confirme o cabo HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                    time.sleep(2)
                                    if(NOS_API.is_signal_present_on_video_source()):
                                        continue   
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI (Não Retestar)")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            else:
                                NOS_API.grabber_stop_video_source()
                                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                                if(NOS_API.is_signal_present_on_video_source()):
                                    ### Colocar verificacao para verificar se imagem e preta. Caso nao seja, fazer contnue. Verificar com proximos testes e comparar com bancada.
                                    TEST_CREATION_API.write_log_to_file("No boot")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                    NOS_API.set_error_message("Não arranca")
                                    error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                else:
                                    TEST_CREATION_API.write_log_to_file("No boot")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                                    NOS_API.set_error_message("Não arranca")
                                    error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                                
                            NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                         
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                            
                          
                            return

                        if not (NOS_API.grab_picture("Scart_Image")):
                            TEST_CREATION_API.write_log_to_file("No video SCART.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.scart_image_absence_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.scart_image_absence_error_message)
                            error_codes = NOS_API.test_cases_results_info.scart_image_absence_error_code
                            error_messages = NOS_API.test_cases_results_info.scart_image_absence_error_message
                            NOS_API.set_error_message("Video Scart")
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
            
                            return
                        
                        ## Start grabber device with video on HDMI1
                        NOS_API.grabber_stop_video_source()
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)

                        ## If no signal on HDMI
                        if (NOS_API.wait_for_no_signal_present(5)):
                            NOS_API.display_dialog("Confirme o cabo HDMI e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                            time.sleep(2)
                            if (NOS_API.wait_for_no_signal_present(5)):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI (Não Retestar)")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                
                                return
                    else:
                        NOS_API.grabber_stop_video_source()
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                
            if(counter_ended == True):
                if(NOS_API.is_signal_present_on_video_source()):
                    if not(NOS_API.grab_picture("Noise_HDMI_Image")):
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                    
        
                        return
                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    System_Failure = 2
                else:    
                    TEST_CREATION_API.write_log_to_file("No boot")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.no_boot_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.no_boot_error_message)
                    NOS_API.set_error_message("Nao arranca")
                    error_codes = NOS_API.test_cases_results_info.no_boot_error_code
                    error_messages = NOS_API.test_cases_results_info.no_boot_error_message
                    System_Failure = 2
            elif((signal_detected_on_hdmi == True) and (signal_detected_on_cvbs == True)):
                if (sw_upgrade_detected):
                    if not(Nagra_Upgrade):
                        result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_started_via_ota"], 30, ["[WRITE_SW_HDMI]"], [80])
                        if (result != -1 and result != -2):
                            result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_progress_ref"], 400, ["[WRITE_SW_HDMI]"], [80])
                            if (result != -1 and result != -2):                            
                                if (NOS_API.wait_for_no_signal_present(90)):
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                    if not(NOS_API.wait_for_signal_present(25)):
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(15)
                                    NOS_API.test_cases_results_info.channel_boot_up_state = True
                                    test_result = "PASS"
                                    result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref"], 35, ["[FULL_SCREEN]"], [80])
                                    result_1 = NOS_API.wait_for_multiple_pictures(["Check_Nagra_1080_ref"], 35, ["[FULL_SCREEN]"], [80])
                                    if (result != -1 and result != -2):
                                        if not(NOS_API.grab_picture("Check_Nagra")):
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                            
                                            return
                                        time.sleep(120)
                                    elif (result_1 != -1 and result_1 != -2):
                                        if not(NOS_API.grab_picture("Check_Nagra")):
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                            
                                            return
                                        time.sleep(120)
                                        
                                    if not(NOS_API.grab_picture("Upgrade_Error")):
                                        test_result = "FAIL"
                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        "",
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                        
                                        return
                                    
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if (video_height == "1080"):
                                        if(TEST_CREATION_API.compare_pictures("Sw_Upgrade_Error_ref", "Upgrade_Error", "[Upgrade_Error]")):
                                            test_result = "FAIL"
                                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                            NOS_API.set_error_message("Não Actualiza")
                                            error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                            
                                    System_Failure = 2        
                                    
                                else:
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                    NOS_API.set_error_message("Não Actualiza")
                                    error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                    System_Failure = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                NOS_API.set_error_message("Não Actualiza")
                                error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                System_Failure = 2
                        else:
                            if (result == -2):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                
                                return
                    else:
                        if not(NOS_API.grab_picture("Check_Nagra")):
                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                            NOS_API.set_error_message("Video HDMI")
                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                            
                            NOS_API.add_test_case_result_to_file_report(
                                            test_result,
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            "- - - - - - - - - - - - - - - - - - - -",
                                            error_codes,
                                            error_messages)
                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
            
                            ## Update test result
                            TEST_CREATION_API.update_test_result(test_result)
                            
                            ## Return DUT to initial state and de-initialize grabber device
                            NOS_API.deinitialize()
                            
                            NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)
                        
            
                            return
                        NOS_API.test_cases_results_info.DidUpgrade = 1
                        NOS_API.test_cases_results_info.channel_boot_up_state = True
                        test_result = "PASS"
                        time.sleep(120)
                        
                        video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                        if (video_height == "1080"):
                            if not(NOS_API.grab_picture("Upgrade_Error")):
                                test_result = "FAIL"
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                
                                return
                        
                            if(TEST_CREATION_API.compare_pictures("Sw_Upgrade_Error_ref", "Upgrade_Error", "[Upgrade_Error]")):
                                test_result = "FAIL"
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                NOS_API.set_error_message("Não Actualiza")
                                error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                
                        System_Failure = 2
                elif (NOS_API.test_cases_results_info.channel_boot_up_state == False):
                    #TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_Check_IR]")
                    #if not(NOS_API.grab_picture("IR_Picture")):
                    #    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    #    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                    #                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    #    NOS_API.set_error_message("Video HDMI")
                    #    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    #    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    #    
                    #    NOS_API.add_test_case_result_to_file_report(
                    #                    test_result,
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    "- - - - - - - - - - - - - - - - - - - -",
                    #                    error_codes,
                    #                    error_messages)
                    #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #    report_file = NOS_API.create_test_case_log_file(
                    #                    NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                    NOS_API.test_cases_results_info.nos_sap_number,
                    #                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                    "",
                    #                    end_time)
                    #    NOS_API.upload_file_report(report_file)
                    #    NOS_API.test_cases_results_info.isTestOK = False
                    #
                    #    ## Update test result
                    #    TEST_CREATION_API.update_test_result(test_result)
                    #    
                    #    ## Return DUT to initial state and de-initialize grabber device
                    #    NOS_API.deinitialize()
                    #    
                    #    NOS_API.send_report_over_mqtt_test_plan(
                    #            test_result,
                    #            end_time,
                    #            error_codes,
                    #            report_file)
                    #
                    #
                    #    return
                    #
                    #video_result = NOS_API.compare_pictures("ref", "IR_Picture", "[FULL_SCREEN]")
                    #video_result_1 = NOS_API.compare_pictures("ref", "IR_Picture", "[FULL_SCREEN]")
                    #
                    #if not(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    #    TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_Check_IR]")
                    #    if not(NOS_API.grab_picture("IR_Picture_2")):
                    #        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    #        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                    #                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    #        NOS_API.set_error_message("Video HDMI")
                    #        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    #        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    #        
                    #        NOS_API.add_test_case_result_to_file_report(
                    #                        test_result,
                    #                        "- - - - - - - - - - - - - - - - - - - -",
                    #                        "- - - - - - - - - - - - - - - - - - - -",
                    #                        error_codes,
                    #                        error_messages)
                    #        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #        report_file = NOS_API.create_test_case_log_file(
                    #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                        NOS_API.test_cases_results_info.nos_sap_number,
                    #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                        "",
                    #                        end_time)
                    #        NOS_API.upload_file_report(report_file)
                    #        NOS_API.test_cases_results_info.isTestOK = False
                    #
                    #        ## Update test result
                    #        TEST_CREATION_API.update_test_result(test_result)
                    #        
                    #        ## Return DUT to initial state and de-initialize grabber device
                    #        NOS_API.deinitialize()
                    #        
                    #        NOS_API.send_report_over_mqtt_test_plan(
                    #                test_result,
                    #                end_time,
                    #                error_codes,
                    #                report_file)
                    #    
                    #
                    #        return
                    #
                    #    video_result = NOS_API.compare_pictures("ref", "IR_Picture_2", "[FULL_SCREEN]")
                    #    video_result_1 = NOS_API.compare_pictures("ref", "IR_Picture_2", "[FULL_SCREEN]")
                    #    
                    #    if not(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD or video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    #        TEST_CREATION_API.write_log_to_file("STB didn't receive IR command")
                    #        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                    #        + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                    #        NOS_API.set_error_message("IR")
                    #        error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                    #        error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                    #        
                    #        NOS_API.add_test_case_result_to_file_report(
                    #                        test_result,
                    #                        "- - - - - - - - - - - - - - - - - - - -",
                    #                        "- - - - - - - - - - - - - - - - - - - -",
                    #                        error_codes,
                    #                        error_messages)
                    #        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #        report_file = NOS_API.create_test_case_log_file(
                    #                        NOS_API.test_cases_results_info.s_n_using_barcode,
                    #                        NOS_API.test_cases_results_info.nos_sap_number,
                    #                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                    #                        "",
                    #                        end_time)
                    #        NOS_API.upload_file_report(report_file)
                    #        NOS_API.test_cases_results_info.isTestOK = False
                    #
                    #        ## Update test result
                    #        TEST_CREATION_API.update_test_result(test_result)
                    #        
                    #        ## Return DUT to initial state and de-initialize grabber device
                    #        NOS_API.deinitialize()
                    #        
                    #        NOS_API.send_report_over_mqtt_test_plan(
                    #                test_result,
                    #                end_time,
                    #                error_codes,
                    #                report_file)
                    #    
                    #
                    #        return
                    #        
                    #TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_Check_IR_2]")
                    
                    TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_BOOT_UP_SEQUENCE_1]")
                    
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height == "1080"):
                        macro_signal_level = "[SIGNAL_VALUE_FTI_50_PERCENT_1080p]"
                        macro_signal_quality = "[SIGNAL_QUALITY_FTI_50_PERCENT_1080p]"
                        macro_right_place = "[FTI_Signal_1080]"
                        ref_image = "signal_value_fti_1080_ref"
                    else:
                        macro_signal_level = "[SIGNAL_VALUE_FTI_50_PERCENT]"
                        macro_signal_quality = "[SIGNAL_QUALITY_FTI_50_PERCENT]"
                        macro_right_place = "[FTI_Signal]"
                        ref_image = "signal_value_fti_ref"
                    
                    if (NOS_API.grab_picture("signal_value")):
                        video_result = NOS_API.compare_pictures(ref_image, "signal_value", macro_right_place)
                        if not(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            TEST_CREATION_API.send_ir_rc_command("[Back_Left]")
                            time.sleep(1)
                            TEST_CREATION_API.send_ir_rc_command("[INSTALLATION_BOOT_UP_SEQUENCE_1]")
                            if not(NOS_API.grab_picture("signal_value")):
                                TEST_CREATION_API.write_log_to_file("STB lost signal on HDMI. Probably reboots.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                            
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                return
                            video_result_1 = NOS_API.compare_pictures(ref_image, "signal_value", macro_right_place)
                            if not(video_result_1 >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.write_log_to_file("STB didn't receive IR command")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ir_nok_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.ir_nok_error_message)
                                NOS_API.set_error_message("IR")
                                error_codes = NOS_API.test_cases_results_info.ir_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.ir_nok_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                        
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                                return
                        try:
                            signal_value = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_level)
                            signal_quality = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_quality)
                        
                        except Exception as error:
                            TEST_CREATION_API.write_log_to_file(str(error))
                            signal_value = 0
                            signal_quality = 0
                            test_result = "FAIL"
                                               
                        ## Check if signal value higher than threshold
                        if not(signal_value >= THRESHOLD and signal_quality >= THRESHOLD): 
                            result = NOS_API.wait_for_multiple_pictures(["Signal_Parameters_ref"], 5, ["[Signal_Parameters]"], [80])
                            if (result != -1 and result != -2):
                                if not(NOS_API.grab_picture("Check_Signal_Parameters")):
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                    
                                    return
                                TEST_CREATION_API.send_ir_rc_command("[Change_Signal_Parameters]")
                                
                                if not(NOS_API.grab_picture("signal_value")):
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                    
                                    return
                                try:
                                    signal_value = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_level)
                                    signal_quality = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_quality)
                                
                                except Exception as error:
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    signal_value = 0
                                    signal_quality = 0
                                    test_result = "FAIL"
                                
                        ## Check if signal value higher than threshold
                        if not(signal_value >= THRESHOLD and signal_quality >= THRESHOLD):
                            NOS_API.display_custom_dialog("Confirme Cabo RF e restantes cabos", 1, ["Continuar"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG)
                            time.sleep(2)
                            if not(NOS_API.grab_picture("signal_value")):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                
                                return
                            try:
                                signal_value = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_level)
                                signal_quality = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_quality)
                            
                            except Exception as error:
                                TEST_CREATION_API.write_log_to_file(str(error))
                                signal_value = 0
                                signal_quality = 0
                                test_result = "FAIL"
                                
                        ## Check if signal value higher than threshold
                        if (signal_value >= THRESHOLD and signal_quality >= THRESHOLD):
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            result = NOS_API.wait_for_multiple_pictures(["scan_complete_ref", "scan_complete_1080p_ref"], 35, ["[SCAN_COMPLETED]", "[SCAN_COMPLETED_1080p]"], [80, 80])
                            
                            if (result == -2):
                                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                NOS_API.set_error_message("Video HDMI")
                                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                
                                NOS_API.add_test_case_result_to_file_report(
                                                test_result,
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                "- - - - - - - - - - - - - - - - - - - -",
                                                error_codes,
                                                error_messages)
                                end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                "",
                                                end_time)
                                NOS_API.upload_file_report(report_file)
                                NOS_API.test_cases_results_info.isTestOK = False
                
                                ## Update test result
                                TEST_CREATION_API.update_test_result(test_result)
                                
                                ## Return DUT to initial state and de-initialize grabber device
                                NOS_API.deinitialize()
                                
                                NOS_API.send_report_over_mqtt_test_plan(
                                        test_result,
                                        end_time,
                                        error_codes,
                                        report_file)
                            
                
                                return
                            if (result != -1):
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                time.sleep(3)
                            
                            test_result = "PASS"
                            
                            result = NOS_API.wait_for_multiple_pictures(["new_sw_detected_message_576", "new_sw_detected_message_720", "new_sw_detected_message_1080", "Check_Nagra_ref", "Check_Nagra_1080_ref"], 30, ["[SW_UPGRADE_MESSAGE_576]", "[SW_UPGRADE_MESSAGE_720]", "[SW_UPGRADE_MESSAGE_1080]", "[Nagra_Upgrade]", "[Nagra_Upgrade_1080]"], [80, 80, 80, 80, 80])
                            if(result == 3 or result == 4):
                                Nagra_Upgrade = True
                            if (result != -1 and result != -2):
                                if not(Nagra_Upgrade): 
                                    result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_started_via_ota"], 30, ["[WRITE_SW_HDMI]"], [80])
                                    if (result != -1 and result != -2):
                                        result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_progress_ref"], 400, ["[WRITE_SW_HDMI]"], [80])
                                        if (result != -1 and result != -2):
                                            if (NOS_API.wait_for_no_signal_present(90)):
                                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                                if not(NOS_API.wait_for_signal_present(25)):
                                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                time.sleep(15)
                                                result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref"], 35, ["[FULL_SCREEN]"], [80])
                                                result_1 = NOS_API.wait_for_multiple_pictures(["Check_Nagra_1080_ref"], 35, ["[FULL_SCREEN]"], [80])
                                                if (result != -1 and result != -2):
                                                    if not(NOS_API.grab_picture("Check_Nagra")):
                                                        test_result = "FAIL"
                                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                        NOS_API.set_error_message("Video HDMI")
                                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        "",
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                    
                                        
                                                        return
                                                    time.sleep(120)  
                                                elif (result_1 != -1 and result_1 != -2):
                                                    if not(NOS_API.grab_picture("Check_Nagra")):
                                                        test_result = "FAIL"
                                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                        NOS_API.set_error_message("Video HDMI")
                                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        "",
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                    
                                        
                                                        return
                                                    time.sleep(120)
                                                    
                                                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                                if (video_height == "1080"):    
                                                    if not(NOS_API.grab_picture("Upgrade_Error")):
                                                        test_result = "FAIL"
                                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                        NOS_API.set_error_message("Video HDMI")
                                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                                        
                                                        NOS_API.add_test_case_result_to_file_report(
                                                                        test_result,
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                                        error_codes,
                                                                        error_messages)
                                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                                        report_file = NOS_API.create_test_case_log_file(
                                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                                        "",
                                                                        end_time)
                                                        NOS_API.upload_file_report(report_file)
                                                        NOS_API.test_cases_results_info.isTestOK = False
                                        
                                                        ## Update test result
                                                        TEST_CREATION_API.update_test_result(test_result)
                                                        
                                                        ## Return DUT to initial state and de-initialize grabber device
                                                        NOS_API.deinitialize()
                                                        
                                                        NOS_API.send_report_over_mqtt_test_plan(
                                                                test_result,
                                                                end_time,
                                                                error_codes,
                                                                report_file)
                                                    
                                        
                                                        return
                                                
                                                    if(TEST_CREATION_API.compare_pictures("Sw_Upgrade_Error_ref", "Upgrade_Error", "[Upgrade_Error]")):
                                                        test_result = "FAIL"
                                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade on HDMI")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                                        NOS_API.set_error_message("Não Actualiza")
                                                        error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                                        
                                                System_Failure = 2
                                                #NOS_API.test_cases_results_info.channel_boot_up_state = True
                                            else:
                                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade on HDMI")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                                NOS_API.set_error_message("Não Actualiza")
                                                error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                                test_result = "FAIL"
                                                System_Failure = 2
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                            NOS_API.set_error_message("Não Actualiza")
                                            error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                            test_result = "FAIL"
                                            System_Failure = 2
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                        NOS_API.set_error_message("Não Actualiza")
                                        error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                        error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                        test_result = "FAIL"
                                        System_Failure = 2
                                else:                                    
                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                    if not(NOS_API.grab_picture("Check_Nagra")):
                                        test_result = "FAIL"
                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        
                                        NOS_API.add_test_case_result_to_file_report(
                                                        test_result,
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        "- - - - - - - - - - - - - - - - - - - -",
                                                        error_codes,
                                                        error_messages)
                                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        report_file = NOS_API.create_test_case_log_file(
                                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                                        NOS_API.test_cases_results_info.nos_sap_number,
                                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                        "",
                                                        end_time)
                                        NOS_API.upload_file_report(report_file)
                                        NOS_API.test_cases_results_info.isTestOK = False
                        
                                        ## Update test result
                                        TEST_CREATION_API.update_test_result(test_result)
                                        
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
                                        
                                        NOS_API.send_report_over_mqtt_test_plan(
                                                test_result,
                                                end_time,
                                                error_codes,
                                                report_file)
                                    
                        
                                        return
                                    time.sleep(120)
                                    
                                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                                    if (video_height == "1080"): 
                                        if not(NOS_API.grab_picture("Upgrade_Error")):
                                            test_result = "FAIL"
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            
                                            NOS_API.add_test_case_result_to_file_report(
                                                            test_result,
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            "- - - - - - - - - - - - - - - - - - - -",
                                                            error_codes,
                                                            error_messages)
                                            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            report_file = NOS_API.create_test_case_log_file(
                                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                                            NOS_API.test_cases_results_info.nos_sap_number,
                                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                            "",
                                                            end_time)
                                            NOS_API.upload_file_report(report_file)
                                            NOS_API.test_cases_results_info.isTestOK = False
                            
                                            ## Update test result
                                            TEST_CREATION_API.update_test_result(test_result)
                                            
                                            ## Return DUT to initial state and de-initialize grabber device
                                            NOS_API.deinitialize()
                                            
                                            NOS_API.send_report_over_mqtt_test_plan(
                                                    test_result,
                                                    end_time,
                                                    error_codes,
                                                    report_file)
                                        
                            
                                            return
                                        
                                        if(TEST_CREATION_API.compare_pictures("Sw_Upgrade_Error_ref", "Upgrade_Error", "[Upgrade_Error]")):
                                            test_result = "FAIL"
                                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                            NOS_API.set_error_message("Não Actualiza")
                                            error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                            
                                    System_Failure = 2
                            else:
                                if (result == -2):
                                    test_result = "FAIL"
                                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                    NOS_API.set_error_message("Video HDMI")
                                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                    
                                    NOS_API.add_test_case_result_to_file_report(
                                                    test_result,
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    "- - - - - - - - - - - - - - - - - - - -",
                                                    error_codes,
                                                    error_messages)
                                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    "",
                                                    end_time)
                                    NOS_API.upload_file_report(report_file)
                                    NOS_API.test_cases_results_info.isTestOK = False
                    
                                    ## Update test result
                                    TEST_CREATION_API.update_test_result(test_result)
                                    
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
                                    
                                    NOS_API.send_report_over_mqtt_test_plan(
                                            test_result,
                                            end_time,
                                            error_codes,
                                            report_file)
                                
                    
                                    return
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("Signal value is lower than threshold")
                        
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.input_signal_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.input_signal_error_message)
                            NOS_API.set_error_message("Sem Sinal")
                            error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                            error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                            System_Failure = 2
                    else:
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        error_codes = NOS_API.test_cases_results_info.input_signal_error_code
                        error_messages = NOS_API.test_cases_results_info.input_signal_error_message
                        NOS_API.set_error_message("Video HDMI")
                        System_Failure = 2
                else:
                    test_result = "PASS"
                    System_Failure = 2
   
        except Exception as error:
            if(System_Failure == 0):
                System_Failure = System_Failure + 1 
                NOS_API.Inspection = True
                if(System_Failure == 1):
                    try:
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                    try:
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        TEST_CREATION_API.write_log_to_file(error)
                    except: 
                        pass
                if (NOS_API.configure_power_switch_by_inspection()):
                    if not(NOS_API.power_off()): 
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                    test_result,
                                    end_time,
                                    error_codes,
                                    report_file)

                        return
                    time.sleep(10)
                    ## Power on STB with energenie
                    if not(NOS_API.power_on()):
                        TEST_CREATION_API.write_log_to_file("Comunication with PowerSwitch Fails")
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                        NOS_API.set_error_message("Inspection")
                        
                        NOS_API.add_test_case_result_to_file_report(
                                        test_result,
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        "- - - - - - - - - - - - - - - - - - - -",
                                        error_codes,
                                        error_messages)
                        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
                        report_file = ""
                        if (test_result != "PASS"):
                            report_file = NOS_API.create_test_case_log_file(
                                            NOS_API.test_cases_results_info.s_n_using_barcode,
                                            NOS_API.test_cases_results_info.nos_sap_number,
                                            NOS_API.test_cases_results_info.cas_id_using_barcode,
                                            "",
                                            end_time)
                            NOS_API.upload_file_report(report_file)
                            NOS_API.test_cases_results_info.isTestOK = False
                        
                        test_result = "FAIL"
                        
                        ## Update test result
                        TEST_CREATION_API.update_test_result(test_result)
                    
                        ## Return DUT to initial state and de-initialize grabber device
                        NOS_API.deinitialize()
                        
                        NOS_API.send_report_over_mqtt_test_plan(
                                test_result,
                                end_time,
                                error_codes,
                                report_file)
                        
                        return
                    time.sleep(10)
                else:
                    TEST_CREATION_API.write_log_to_file("Incorrect test place name")
                    
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.power_switch_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.power_switch_error_message)
                    NOS_API.set_error_message("Inspection")
                    
                    NOS_API.add_test_case_result_to_file_report(
                                    test_result,
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    "- - - - - - - - - - - - - - - - - - - -",
                                    error_codes,
                                    error_messages)
                    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
                    report_file = ""
                    if (test_result != "PASS"):
                        report_file = NOS_API.create_test_case_log_file(
                                        NOS_API.test_cases_results_info.s_n_using_barcode,
                                        NOS_API.test_cases_results_info.nos_sap_number,
                                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                                        "",
                                        end_time)
                        NOS_API.upload_file_report(report_file)
                        NOS_API.test_cases_results_info.isTestOK = False
                    
                    test_result = "FAIL"
                    ## Update test result
                    TEST_CREATION_API.update_test_result(test_result)
                    
                
                    ## Return DUT to initial state and de-initialize grabber device
                    NOS_API.deinitialize()
                    
                    NOS_API.send_report_over_mqtt_test_plan(
                        test_result,
                        end_time,
                        error_codes,
                        report_file)
                    
                    return
                
                NOS_API.Inspection = False
            else:
                test_result = "FAIL"
                TEST_CREATION_API.write_log_to_file(error)
                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                NOS_API.set_error_message("Inspection")
                System_Failure = 2

    NOS_API.add_test_case_result_to_file_report(
                    test_result,
                    "- - - - - - - - - - - - - - - - - - - -",
                    "- - - - - - - - - - - - - - - - - - - -",
                    error_codes,
                    error_messages)
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    report_file = ""
    if (test_result != "PASS"):
        report_file = NOS_API.create_test_case_log_file(
                        NOS_API.test_cases_results_info.s_n_using_barcode,
                        NOS_API.test_cases_results_info.nos_sap_number,
                        NOS_API.test_cases_results_info.cas_id_using_barcode,
                        "",
                        end_time)
        NOS_API.upload_file_report(report_file)
        NOS_API.test_cases_results_info.isTestOK = False
        
        NOS_API.send_report_over_mqtt_test_plan(
                test_result,
                end_time,
                error_codes,
                report_file)
             
    ## Update test result
    TEST_CREATION_API.update_test_result(test_result)

    ## Return DUT to initial state and de-initialize grabber device
    NOS_API.deinitialize()