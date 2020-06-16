# -*- coding: utf-8 -*-
# Test name = Autodiag1
# Test description = SC detection

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

def runTest():
    
    System_Failure = 0
    
    while (System_Failure < 2):
    
        try:   

            ## Set test result default to FAIL
            test_result = "FAIL"
            
            error_codes = ""
            error_messages = ""
            
            counter = 0
            result = 0
            result_1 = 0
            answer = 0
            repeat = 0
            
            ## Initialize grabber device
            TEST_CREATION_API.initialize_grabber()
            
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)       
            
            #if not(NOS_API.change_usb_port("USBHUB-01##")):
            #    TEST_CREATION_API.write_log_to_file("USB on port 1 is not enabled")
            #    NOS_API.test_cases_results_info.isTestOK = False
            #    TEST_CREATION_API.update_test_result(test_result)
            #    NOS_API.set_error_message("Inspection")
            #    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.usb_hub_error_code \
            #                                        + "; Error message: " + NOS_API.test_cases_results_info.usb_hub_error_message)
            #    error_codes = NOS_API.test_cases_results_info.usb_hub_error_code
            #    error_messages = NOS_API.test_cases_results_info.usb_hub_error_message
            #    ## Return DUT to initial state and de-initialize grabber device
            #    NOS_API.deinitialize()
            #    NOS_API.add_test_case_result_to_file_report(
            #            test_result,
            #            "- - - - - - - - - - - - - - - - - - - -",
            #            "- - - - - - - - - - - - - - - - - - - -",
            #            error_codes,
            #            error_messages)
            #    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
            #    report_file = NOS_API.create_test_case_log_file(
            #                NOS_API.test_cases_results_info.s_n_using_barcode,
            #                NOS_API.test_cases_results_info.nos_sap_number,
            #                NOS_API.test_cases_results_info.cas_id_using_barcode,
            #                "",
            #                end_time)
            #    NOS_API.upload_file_report(report_file)
            #    
            #    NOS_API.send_report_over_mqtt_test_plan(
            #        test_result,
            #        end_time,
            #        error_codes,
            #        report_file)
            #
            #    return
                
            time.sleep(3)
            
            ## Enter autodiag
            TEST_CREATION_API.send_ir_rc_command("[POWER]")
            time.sleep(1)
            
            while(counter < 2):
                if repeat == 0:
                    if counter == 1:
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
                        time.sleep(4)
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
                        time.sleep(22)
                        if(NOS_API.is_signal_present_on_video_source()):
                            TEST_CREATION_API.send_ir_rc_command("[POWER]")
                            time.sleep(5)
                            if (NOS_API.is_signal_present_on_video_source()):
                                TEST_CREATION_API.send_ir_rc_command("[POWER]")
                    if (NOS_API.is_signal_present_on_video_source()):
                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                        time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[ENTER_AUTODIAG_new]")
                
                    result = NOS_API.wait_for_multiple_pictures(["AutoDiag_ref"], 45, ["[Enter_AutoDiag]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD])       
                    if not(result != -1 and result != -2):
                        if(counter == 1):  
                            counter = counter + 1
                            TEST_CREATION_API.write_log_to_file("Autodiag failed")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                            NOS_API.set_error_message("AutoDiag")
                            error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                            error_messages = NOS_API.test_cases_results_info.autodiag_error_message

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
                            return
                        else:
                            counter = counter + 1
                            continue
                    if not(NOS_API.grab_picture("AutoDiag")):
                        TEST_CREATION_API.write_log_to_file("HDMI NOK")
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
                        return
                    
                    video_result = NOS_API.compare_pictures("AutoDiag_new_ref", "AutoDiag", "[AutoDiag_new]")
                    if (video_result < TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):  
                        
                        TEST_CREATION_API.send_ir_rc_command("[RED]")
                        time.sleep(1)
                        if not(NOS_API.grab_picture("AD_Update")):
                            TEST_CREATION_API.write_log_to_file("HDMI NOK")
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
                            return
                        
                        if not(TEST_CREATION_API.compare_pictures("AD_Update_ref", "AD_Update", "[AD_Update]")):
                            TEST_CREATION_API.send_ir_rc_command("[RED]")
                            time.sleep(1)
                            if not(NOS_API.grab_picture("AD_Update_2")):
                                TEST_CREATION_API.write_log_to_file("HDMI NOK")
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
                                return
                            if not(TEST_CREATION_API.compare_pictures("AD_Update_ref", "AD_Update_2", "[AD_Update]")):
                                TEST_CREATION_API.write_log_to_file("Error Updating AD")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                                NOS_API.set_error_message("AutoDiag")
                                error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                                error_messages = NOS_API.test_cases_results_info.autodiag_error_message
                                
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
                        if(NOS_API.wait_for_no_signal_present(60)):
                            time.sleep(10)
                            TEST_CREATION_API.send_ir_rc_command("[ENTER_AUTODIAG_new]")
                        else:
                            if(counter == 1):  
                                counter = counter + 1
                                TEST_CREATION_API.write_log_to_file("Autodiag failed")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                                NOS_API.set_error_message("AutoDiag")
                                error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                                error_messages = NOS_API.test_cases_results_info.autodiag_error_message
                                
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
                                counter = counter + 1
                                continue
                                           
                    if not(NOS_API.wait_for_signal_present(50)):
                        if(counter == 1):  
                            counter = counter + 1
                            TEST_CREATION_API.write_log_to_file("Autodiag failed")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                            NOS_API.set_error_message("AutoDiag")
                            error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                            error_messages = NOS_API.test_cases_results_info.autodiag_error_message
                            
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
                            return
                        else:
                            counter = counter + 1
                            continue
                    result_1 = NOS_API.wait_for_multiple_pictures(["AutoDiag_ref"], 45, ["[Enter_AutoDiag]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD])
                    if not(result_1 != -1 and result_1 != -2):
                        if(counter == 1):  
                            if(result_1 != -2):
                                counter = counter + 1
                                TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                                NOS_API.set_error_message("Reboot")
                                error_codes = NOS_API.test_cases_results_info.reboot_error_code
                                error_messages = NOS_API.test_cases_results_info.reboot_error_message
                            else:
                                counter = counter + 1
                                TEST_CREATION_API.write_log_to_file("Autodiag failed")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.autodiag_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.autodiag_error_message)
                                NOS_API.set_error_message("AutoDiag")
                                error_codes = NOS_API.test_cases_results_info.autodiag_error_code
                                error_messages = NOS_API.test_cases_results_info.autodiag_error_message

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
                            return
                        else:
                            counter = counter + 1
                            continue
                    
                if answer == 0:    
                    if not(NOS_API.display_custom_dialog("O Led Power est\xe1 Vermelho?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("Led Red NOK")  
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.led_power_red_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.led_power_red_nok_error_message)
                        NOS_API.set_error_message("Led's")
                        error_codes = NOS_API.test_cases_results_info.led_power_red_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.led_power_red_nok_error_message
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
                        return
                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                    if not(NOS_API.display_custom_dialog("O Led Power est\xe1 Verde?", 2, ["OK", "NOK"], NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "OK"):
                        TEST_CREATION_API.write_log_to_file("Led Green NOK") 
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.led_power_green_nok_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.led_power_green_nok_error_message)
                        NOS_API.set_error_message("Led's")
                        error_codes = NOS_API.test_cases_results_info.led_power_green_nok_error_code
                        error_messages = NOS_API.test_cases_results_info.led_power_green_nok_error_message
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
                        return
                        
                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                    time.sleep(1)
                    answer = 1
                else:
                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                    time.sleep(1)
                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                    time.sleep(1)

                TEST_CREATION_API.send_ir_rc_command("[OK]")
                time.sleep(3)
                if not(NOS_API.grab_picture("USB_Check")):
                    TEST_CREATION_API.write_log_to_file("HDMI NOK")
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
                    return
                if (TEST_CREATION_API.compare_pictures("USB_AD_ref", "USB_Check", "[Check_USB]")):
                    TEST_CREATION_API.send_ir_rc_command("[OK]")                              
                if not(NOS_API.wait_for_multiple_pictures(["AutoDiag_End_ref"], 60, ["[AutoDiag_End]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                    video_result = NOS_API.compare_pictures("Blocks_Image_ref", "DUT_snapshot_name", "[Block_Image]")
                    if (video_result > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        if not(NOS_API.wait_for_multiple_pictures(["AutoDiag_End_ref"], 60, ["[AutoDiag_End]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                            if counter == 0:
                                counter += 1
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("STB Blocks on AutoDiag Test")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.block_error_message )
                                NOS_API.set_error_message("STB bloqueou")
                                error_codes = NOS_API.test_cases_results_info.block_error_code
                                error_messages = NOS_API.test_cases_results_info.block_error_message 
                                test_result = "FAIL"

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
                                return
                    else:
                        if counter == 1:
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
                            return           
                        else:
                            counter += 1
                            continue
                if (NOS_API.wait_for_multiple_pictures(["AutoDiag_End_ref"], 60, ["[AutoDiag_End]"], [TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD]) != -1):
                    video_result = NOS_API.compare_pictures("AutoDiag_End_ref", "DUT_snapshot_name", "[AutoDiag_Pass]")
                    if (video_result > TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                        test_result = "PASS"
                        counter = 2
                        NOS_API.Send_Serial_Key("d", "feito")
                        NOS_API.configure_power_switch_by_inspection()
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
                        time.sleep(1)  
                        System_Failure = 2
                    else:                          
                        data_array = NOS_API.get_pixels_average_values("DUT_snapshot_name", 295, 86, 314, 102)
                        TEST_CREATION_API.write_log_to_file(data_array[1] - data_array[0])
                        if (data_array[1] - data_array[0] < 45):
                            TEST_CREATION_API.write_log_to_file("Led's NOK")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.leds_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.leds_nok_error_message)
                            NOS_API.set_error_message("Led's")
                            error_codes = NOS_API.test_cases_results_info.leds_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.leds_nok_error_message
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
                            return                            
                        data_array = NOS_API.get_pixels_average_values("DUT_snapshot_name", 225, 115, 245, 130)
                        TEST_CREATION_API.write_log_to_file(data_array[1] - data_array[0])
                        if (data_array[1] - data_array[0] < 45):
                            if counter == 0:
                                NOS_API.display_dialog("Confirme o cabo USB e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                counter += 1
                                repeat += 1
                                TEST_CREATION_API.send_ir_rc_command("[Repeat_AD]")
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("USB test failed")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.usb_nok_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.usb_nok_error_message)
                                NOS_API.set_error_message("USB")
                                error_codes = NOS_API.test_cases_results_info.usb_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.usb_nok_error_message
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
                                return                           
                        data_array = NOS_API.get_pixels_average_values("DUT_snapshot_name", 236, 144, 255, 157)
                        TEST_CREATION_API.write_log_to_file(data_array[1] - data_array[0])
                        if (data_array[1] - data_array[0] < 45):
                            TEST_CREATION_API.write_log_to_file("Flash test failed")
                            NOS_API.set_error_message("IC")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.flash_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.flash_nok_error_message)
                            error_codes = NOS_API.test_cases_results_info.flash_nok_error_code
                            error_messages = NOS_API.test_cases_results_info.flash_nok_error_message
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
                            return
                        data_array = NOS_API.get_pixels_average_values("DUT_snapshot_name", 278, 172, 295, 184)
                        TEST_CREATION_API.write_log_to_file(data_array[1] - data_array[0])
                        if (data_array[1] - data_array[0] < 45):
                            if counter == 0:
                                NOS_API.display_dialog("Confirme o cabo ETH e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                counter += 1
                                repeat += 1
                                TEST_CREATION_API.send_ir_rc_command("[Repeat_AD]")
                                continue
                            else:
                                TEST_CREATION_API.write_log_to_file("Ethernet test failed")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ethernet_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.ethernet_nok_error_message)
                                NOS_API.set_error_message("Eth")
                                error_codes = NOS_API.test_cases_results_info.ethernet_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.ethernet_nok_error_message
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
                                return
                        data_array = NOS_API.get_pixels_average_values("DUT_snapshot_name", 334, 201, 349, 213)
                        TEST_CREATION_API.write_log_to_file(data_array[1] - data_array[0])
                        if (data_array[1] - data_array[0] < 45):
                            TEST_CREATION_API.write_log_to_file("Factory Reset Test Fail")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.measure_boot_time_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.measure_boot_time_error_message)
                            NOS_API.set_error_message("Factory Reset")
                            error_codes = NOS_API.test_cases_results_info.measure_boot_time_error_code
                            error_messages = NOS_API.test_cases_results_info.measure_boot_time_error_message
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
                            return    
                else:
                    if counter == 0:
                        counter += 1
                        continue
                    else:
                        counter = 2
                        TEST_CREATION_API.write_log_to_file("STB Blocks on AutoDiag Test")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.block_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.block_error_message )
                        NOS_API.set_error_message("STB bloqueou")
                        error_codes = NOS_API.test_cases_results_info.block_error_code
                        error_messages = NOS_API.test_cases_results_info.block_error_message 
                        test_result = "FAIL"      
                        
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
