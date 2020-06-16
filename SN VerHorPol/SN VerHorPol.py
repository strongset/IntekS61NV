# -*- coding: utf-8 -*-
# Test name = Serial Number
# Test description = Check S/N from menu with scanned S/N, log nagraguide version and sw version

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

def runTest():

    ## Skip this test case if some of previous tests from test plan failed
    if not(NOS_API.test_cases_results_info.isTestOK):
        TEST_CREATION_API.update_test_result(TEST_CREATION_API.TestCaseResult.FAIL)
        #TEST_CREATION_API.write_log_to_file("Skip this test case if some of previous tests from test plan failed.")
        return
    
    System_Failure = 0
    
    while (System_Failure < 2):
        
        if(System_Failure == 1):
            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
            TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
            TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
    
        try:
            ## Set test result default to FAIL
            test_result = "FAIL"

            error_codes = ""
            error_messages = ""
            
            serial_number_test = False
            test_result_ver = False 
            
            signal_strength_ver = "-"
            ber_ver = "-"
            signal_strength_hor = "-"
            ber_hor = "-"
            
            power_percentage = "-"
            signal_quality_percentage = "-"
            logistic_serial_number = "-"
            nagra_guide_version = "-"
            firmware_version = "-"
            sc_number = "-"
            cas_id_number = "-"
            FIRMWARE_VERSION_PROD = NOS_API.Firmware_Version_Intek
            nagra_guide_version_Prod = NOS_API.Nagra_Guide_Version_Intek

            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            time.sleep(1)

            if (NOS_API.is_signal_present_on_video_source()):
                
                #if (NOS_API.test_cases_results_info.channel_boot_up_state):
                #    ## Set language to Portugal if not set
                #    TEST_CREATION_API.send_ir_rc_command("[Info_Box]")
                #else:  
                ## Perform grab picture
                if not(NOS_API.grab_picture("Block_Check_Image")):
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
                TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU_NEW]")
                time.sleep(1)
                ## Perform grab picture
                if not(NOS_API.grab_picture("settings")):
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
                if(TEST_CREATION_API.compare_pictures("Block_Check_Image", "settings", "[FULL_SCREEN]")):
                    TEST_CREATION_API.write_log_to_file("STB Blocks")
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
                
                if not(TEST_CREATION_API.compare_pictures("zon_box_data_ref", "settings", "[ZON_BOX]") or TEST_CREATION_API.compare_pictures("zon_box_data_ref_1", "settings", "[ZON_BOX]")):
                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                    ## Navigate to the Info ZON box menu
                    TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU_NEW]")

                    if not(NOS_API.grab_picture("settings")):
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
                    
                    if not(TEST_CREATION_API.compare_pictures("zon_box_data_ref", "settings", "[ZON_BOX]") or TEST_CREATION_API.compare_pictures("zon_box_data_ref_1", "settings", "[ZON_BOX]")):
                        TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                        NOS_API.set_error_message("Navegação")
                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                            NOS_API.test_cases_results_info.mac_using_barcode,
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
                         
                ## Check language
                if not(TEST_CREATION_API.compare_pictures("sc_info_ref", "settings", "[SETTINGS_1]")):
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[SET_LANGUAGE_PORTUGAL_FROM_SETTINGS]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")

                    ## Navigate to the Info ZON box menu
                    TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU_NEW]")
                
                if (NOS_API.grab_picture("zon_box_data")):
                    if not(TEST_CREATION_API.compare_pictures("zon_box_data_ref", "zon_box_data", "[ZON_BOX]") or TEST_CREATION_API.compare_pictures("zon_box_data_ref_1", "zon_box_data", "[ZON_BOX]")):
                        
                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                        ## Navigate to the Info ZON box menu
                        TEST_CREATION_API.send_ir_rc_command("[INFO_ZON_BOX_MENU_NEW]")
                        
                    if (NOS_API.grab_picture("zon_box_data")):
                        
                        if not(TEST_CREATION_API.compare_pictures("zon_box_data_ref", "zon_box_data", "[ZON_BOX]") or TEST_CREATION_API.compare_pictures("zon_box_data_ref_1", "zon_box_data", "[ZON_BOX]")):
                            TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                            NOS_API.set_error_message("Navegação")
                            error_codes = NOS_API.test_cases_results_info.navigation_error_code
                            error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                NOS_API.test_cases_results_info.mac_using_barcode,
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
                          
                        ## Extract serial number from image
                        logistic_serial_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("zon_box_data", "[SERIAL_NUMBER]", "[OCR_FILTER]", "serial_number"))  
                        NOS_API.test_cases_results_info.s_n = logistic_serial_number                  
                        s_n_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.s_n_using_barcode)
            
                        ## Check if logistic serial number is the same as scanned serial number
                        if (NOS_API.ignore_zero_letter_o_during_comparation(logistic_serial_number, s_n_using_barcode)):
            
                            TEST_CREATION_API.write_log_to_file("Logistic serial number (from menu):\t" + logistic_serial_number, "logistic_serial_number.txt")
            
                            ## Extract NagraGuide version from image
                            nagra_guide_version = TEST_CREATION_API.OCR_recognize_text("zon_box_data", "[NAGRA_GUIDE_VERSION]", "[OCR_FILTER]", "nagra_guide_version")
                            NOS_API.test_cases_results_info.nagra_guide_version = nagra_guide_version
            
                            TEST_CREATION_API.write_log_to_file("The extracted nagra guide version is: " + nagra_guide_version)
                            if (nagra_guide_version == nagra_guide_version_Prod):
                                
                                ## Extract SW Version from image
                                firmware_version = TEST_CREATION_API.OCR_recognize_text("zon_box_data", "[FIRMWARE_VERSION]", "[OCR_FILTER]", "firmware_version")
                                firmware_version = NOS_API.replace_letter_o_with_number_0(firmware_version)
                                NOS_API.test_cases_results_info.firmware_version = firmware_version
                
                                TEST_CREATION_API.write_log_to_file("The extracted firmware version is: " + firmware_version)
                                
                                if (firmware_version == FIRMWARE_VERSION_PROD):
                                
                                    ## Navigate to the signal menu to check signal strength and quality
                                    TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    
                                    if (NOS_API.grab_picture("signal")):
                                        try:
                                            power_percentage = NOS_API.replace_missed_chars(TEST_CREATION_API.OCR_recognize_text("signal", "[POWER_PERCENTAGE]", "[OCR_FILTER]"))
                                            #power_percentage = float(power_percentage[:(power_percentage.find('%'))])
                                            if (power_percentage.find('%') != -1):
                                                power_percentage = float(power_percentage[:(power_percentage.find('%'))])
                                            TEST_CREATION_API.write_log_to_file("Power percentage: " + str(power_percentage))
                                            NOS_API.test_cases_results_info.power_percent = str(power_percentage)
                                            
                                                                        
                                            signal_quality_percentage = NOS_API.replace_missed_chars(TEST_CREATION_API.OCR_recognize_text("signal", "[QUALITY_PERCENTAGE]", "[OCR_FILTER]"))
                                            #signal_quality_percentage = float(signal_quality_percentage[:(signal_quality_percentage.find('%'))])
                                            if (signal_quality_percentage.find('%') != -1):
                                                signal_quality_percentage = float(signal_quality_percentage[:(signal_quality_percentage.find('%'))])
                                            TEST_CREATION_API.write_log_to_file("Signal quality percentage: " + str(signal_quality_percentage))
                                            NOS_API.test_cases_results_info.ber_percent = str(signal_quality_percentage)
                                        except Exception as error:
                                            TEST_CREATION_API.write_log_to_file(error)
                                            power_percentage = "-"
                                            signal_quality_percentage = "-"
                                            NOS_API.test_cases_results_info.power_percent = "-"
                                            NOS_API.test_cases_results_info.ber_percent = "-"
                    
                                        # Navigate to the SC information menu
                                        TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                    
                                        ## Perform grab picture
                                        if (NOS_API.grab_picture("sc_info")):
                                            
                                            if not (TEST_CREATION_API.compare_pictures("sc_info_ref", "sc_info", "[Right_Page]")):
                                                if not(NOS_API.grab_picture("SC")):
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
                                                TEST_CREATION_API.send_ir_rc_command("[RIGHT]")
                                                if not(NOS_API.grab_picture("sc_info")):
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
                                                if not (TEST_CREATION_API.compare_pictures("sc_info_ref", "sc_info", "[Right_Page]")):
                                                    TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                                    NOS_API.set_error_message("Navegação")
                                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                                        NOS_API.test_cases_results_info.mac_using_barcode,
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
                                                    
                                            video_result = NOS_API.mask_and_compare_pictures("sc_info_ref", "sc_info", "sc_info_mask")
                    
                                            ## Check is SC not detected
                                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD): 
                               ####################################################################################################################################################################            
                                                NOS_API.display_dialog("Aten\xe7\xe3o! Reinsira o cart\xe3o e de seguida pressiona Continuar", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                                TEST_CREATION_API.write_log_to_file("VAlue1: " + str(video_result))
                                                TEST_CREATION_API.send_ir_rc_command("[REDO_SC]")
                                                
                                                if not(NOS_API.grab_picture("sc_info_REDO")):
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
                                                if not (TEST_CREATION_API.compare_pictures("sc_info_ref", "sc_info_REDO", "[Right_Page]")):                                               
                                                    TEST_CREATION_API.send_ir_rc_command("[REDO_SC]")
                                                    if not(NOS_API.grab_picture("sc_info_REDO_2")):
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
                                                    if not (TEST_CREATION_API.compare_pictures("sc_info_ref", "sc_info_REDO_2", "[Right_Page]")):
                                                        TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                                        NOS_API.set_error_message("Navegação")
                                                        error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                                        error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
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
                                                
                                                ## Perform grab picture
                                                try:
                                                    TEST_CREATION_API.grab_picture("sc_info")
                                                except: 
                                                    time.sleep(5)
                                                    try:
                                                        TEST_CREATION_API.grab_picture("sc_info")
                                                    except:
                                                        
                                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                                        NOS_API.set_error_message("Video HDMI")
                                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
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
                                                                            NOS_API.test_cases_results_info.mac_using_barcode,
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
                                                                            
                                                
                                                
                                                video_result = NOS_API.mask_and_compare_pictures("sc_info_ref", "sc_info", "sc_info_mask")
                                                TEST_CREATION_API.write_log_to_file("VAlue: " + str(video_result))
                                                ## Check is SC not detected
                                                if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                                
                                                    TEST_CREATION_API.write_log_to_file("Smart card is not detected")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.sc_not_detected_error_code \
                                                                                            + "; Error message: " + NOS_API.test_cases_results_info.sc_not_detected_error_message)
                                                    NOS_API.set_error_message("SmartCard")
                                                    error_codes = NOS_API.test_cases_results_info.sc_not_detected_error_code
                                                    error_messages = NOS_API.test_cases_results_info.sc_not_detected_error_message
                                                    System_Failure = 2
                                                else:
                    
                                                    ## Extract text from image
                                                    sc_number = TEST_CREATION_API.OCR_recognize_text("sc_info", "[SC_NUMBER]", "[OCR_FILTER]", "sc_number")
                                                    #cas_id_number = NOS_API.replace_missed_chars(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                                                    cas_id_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                        
                                                    NOS_API.test_cases_results_info.sc_number = sc_number
                                                    NOS_API.test_cases_results_info.cas_id_number = cas_id_number
                        
                                                    TEST_CREATION_API.write_log_to_file("The extracted sc number is: " + sc_number)
                                                    TEST_CREATION_API.write_log_to_file("The extracted cas id number is: " + cas_id_number)
                        
                                                    NOS_API.update_test_slot_comment("SC number: " + NOS_API.test_cases_results_info.sc_number \
                                                                                        + "; cas id number: " + NOS_API.test_cases_results_info.cas_id_number)
                                                                                        
                                                    cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
                        
                                                    ## System must compare CAS ID number with the CAS ID number scanned by barcode scanner
                                                    if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id_number, cas_id_using_barcode)):
                                                        serial_number_test = True
                                                    else:
                                                        TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                                                                                        + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                                                                                        + "; OCR: " + str(cas_id_number))
                                                        NOS_API.set_error_message("CAS ID")
                                                        error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                                                        error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message  
                                                        System_Failure = 2                                                        
                                            else:
                    
                                                ## Extract text from image
                                                sc_number = TEST_CREATION_API.OCR_recognize_text("sc_info", "[SC_NUMBER]", "[OCR_FILTER]", "sc_number")
                                                #cas_id_number = NOS_API.replace_missed_chars(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                                                cas_id_number = NOS_API.remove_whitespaces(TEST_CREATION_API.OCR_recognize_text("sc_info", "[CAS_ID_NUMBER]", "[OCR_FILTER]", "cas_id_number"))
                    
                                                NOS_API.test_cases_results_info.sc_number = sc_number
                                                NOS_API.test_cases_results_info.cas_id_number = cas_id_number
                    
                                                TEST_CREATION_API.write_log_to_file("The extracted sc number is: " + sc_number)
                                                TEST_CREATION_API.write_log_to_file("The extracted cas id number is: " + cas_id_number)
                    
                                                NOS_API.update_test_slot_comment("SC number: " + NOS_API.test_cases_results_info.sc_number \
                                                                                    + "; cas id number: " + NOS_API.test_cases_results_info.cas_id_number)
                                                                                    
                                                cas_id_using_barcode = NOS_API.remove_whitespaces(NOS_API.test_cases_results_info.cas_id_using_barcode)
                    
                                                ## System must compare CAS ID number with the CAS ID number scanned by barcode scanner
                                                if (NOS_API.ignore_zero_letter_o_during_comparation(cas_id_number, cas_id_using_barcode)):
                                                    serial_number_test = True
                                                else:
                                                    TEST_CREATION_API.write_log_to_file("CAS ID number and CAS ID number previuosly scanned by barcode scanner is not the same")
                                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_cas_id_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.wrong_cas_id_error_message \
                                                                                    + "; OCR: " + str(cas_id_number))
                                                    NOS_API.set_error_message("CAS ID")
                                                    error_codes = NOS_API.test_cases_results_info.wrong_cas_id_error_code
                                                    error_messages = NOS_API.test_cases_results_info.wrong_cas_id_error_message
                                                    System_Failure = 2
                                        else:
                                            TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                            NOS_API.set_error_message("Video HDMI")
                                            error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                            error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                            System_Failure = 2
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                                        NOS_API.set_error_message("Video HDMI")
                                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                                        System_Failure = 2
                                else:
                                    TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                    NOS_API.set_error_message("Não Actualiza") 
                                    error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                    error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                    test_result = "FAIL" 
                                    System_Failure = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message) 
                                NOS_API.set_error_message("Não Actualiza") 
                                error_codes =  NOS_API.test_cases_results_info.upgrade_nok_error_code
                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                test_result = "FAIL"
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("Logistic serial number is not the same as scanned serial number")
            
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.wrong_s_n_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.wrong_s_n_error_message \
                                                                        + "; OCR: " + str(logistic_serial_number))
                            NOS_API.set_error_message("S/N")
                            error_codes = NOS_API.test_cases_results_info.wrong_s_n_error_code
                            error_messages = NOS_API.test_cases_results_info.wrong_s_n_error_message
                            System_Failure = 2
                    else:
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        System_Failure = 2
                else:
                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    System_Failure = 2
            else:
                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                       + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                NOS_API.set_error_message("Video HDMI")
                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                System_Failure = 2
     
    #####################################################################################################################################################################################################################################
    ####################################################################################################     Vertical     ###############################################################################################################
    ####################################################################################################   POLARIZATION   ###############################################################################################################
    ##################################################################################################################################################################################################################################### 
            
            if(serial_number_test):
            
                NOS_API.display_dialog("Remova o cart\xe3o e de seguida pressiona Continuar", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                
                if (NOS_API.is_signal_present_on_video_source()):
                            
                    TEST_CREATION_API.send_ir_rc_command("[Ver_Hor_Pol]")
                    if (NOS_API.grab_picture("signal_right_menu")):
                        if not(TEST_CREATION_API.compare_pictures("signal_menu_ref", "signal_right_menu", "[CANAIS_MENU]")):
                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                            TEST_CREATION_API.send_ir_rc_command("[SIGNAL_MENU]")      
                            ## Perform grab picture                
                            if (NOS_API.grab_picture("signal_right_menu_1")):
                                if not(TEST_CREATION_API.compare_pictures("signal_menu_ref", "signal_right_menu_1", "[CANAIS_MENU]")):
                                    TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                    NOS_API.set_error_message("Navegação")
                                    error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                    error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                        NOS_API.test_cases_results_info.mac_using_barcode,
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
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
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
                        ## Zap to vertical polarization channel
                        TEST_CREATION_API.send_ir_rc_command(NOS_API.VERTICAL_POLARIZATION_CHANNEL_NUMBER)
                        time.sleep(1)
                        
                        if not(NOS_API.grab_picture("signal_menu_ver")):
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
                            report_file = ""    
                            if (test_result != "PASS"):
                                report_file = NOS_API.create_test_case_log_file(
                                                NOS_API.test_cases_results_info.s_n_using_barcode,
                                                NOS_API.test_cases_results_info.nos_sap_number,
                                                NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                NOS_API.test_cases_results_info.mac_using_barcode,
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
                        if not(TEST_CREATION_API.compare_pictures("signal_menu_ref", "signal_menu_ver", "[AlJazeera]")):
                            time.sleep(1)
                            ## Zap to vertical polarization channel
                            TEST_CREATION_API.send_ir_rc_command(NOS_API.VERTICAL_POLARIZATION_CHANNEL_NUMBER)
                            time.sleep(1)
                            if not(NOS_API.grab_picture("signal_menu_ver")):
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
                                report_file = ""    
                                if (test_result != "PASS"):
                                    report_file = NOS_API.create_test_case_log_file(
                                                    NOS_API.test_cases_results_info.s_n_using_barcode,
                                                    NOS_API.test_cases_results_info.nos_sap_number,
                                                    NOS_API.test_cases_results_info.cas_id_using_barcode,
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
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
                            if not(TEST_CREATION_API.compare_pictures("signal_menu_ref", "signal_menu_ver", "[AlJazeera]")):
                                TEST_CREATION_API.write_log_to_file("Doesn't Navigate to right place")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.navigation_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.navigation_error_message)
                                NOS_API.set_error_message("Navegação")
                                error_codes = NOS_API.test_cases_results_info.navigation_error_code
                                error_messages = NOS_API.test_cases_results_info.navigation_error_message
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
                                                    NOS_API.test_cases_results_info.mac_using_barcode,
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
                            
                        try:
                            ## Extract text from image
                            signal_strength_ver = NOS_API.replace_missed_chars_with_numbers(TEST_CREATION_API.OCR_recognize_text("signal_menu_ver", "[POWER_CANAIS_MENU]", "[OCR_FILTER]"))
                            TEST_CREATION_API.write_log_to_file("OCR: " + str(signal_strength_ver))
                            if not(NOS_API.represent_float(signal_strength_ver)):
                                signal_strength_ver = 17
                            else:
                                signal_strength_ver = float(signal_strength_ver)                                               
                        
                            TEST_CREATION_API.write_log_to_file("Power vertical polarization: " + str(signal_strength_ver) + "dBuV")
                            NOS_API.update_test_slot_comment("Power vertical polarization: " + str(signal_strength_ver) + "dBuV")
                            NOS_API.test_cases_results_info.power_vertical_polarization = str(signal_strength_ver)
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            signal_strength_ver = 17
                            NOS_API.test_cases_results_info.power_vertical_polarization = "-"                 
                        
                        if(NOS_API.validate_threshold_range(signal_strength_ver, NOS_API.thresholds_info.power_vertical) == True):
                            try:            
                                ber_ver = NOS_API.fix_ber(TEST_CREATION_API.OCR_recognize_text("signal_menu_ver", "[BER_CANAIS_MENU]", "[OCR_FILTER]"))
                                TEST_CREATION_API.write_log_to_file("BER vertical polarization: " + ber_ver)
                                NOS_API.update_test_slot_comment("BER vertical polarization: " + ber_ver)
                                NOS_API.test_cases_results_info.ber_vertical_polarization = ber_ver
                                #ber_ver = float(ber_ver)
                                
                            except Exception as error:                           
                                ber_ver = "-"
                                NOS_API.test_cases_results_info.ber_vertical_polarization = "-"

                            if(NOS_API.validate_threshold_range(ber_ver, NOS_API.thresholds_info.ber_vertical, True) == True):
                                test_result_ver = True
                            else:
                                TEST_CREATION_API.write_log_to_file("Ber on vertical polarization")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ber_vertical_polarization_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.ber_vertical_polarization_error_message)
                                NOS_API.set_error_message("Tuner") 
                                error_codes = NOS_API.test_cases_results_info.ber_vertical_polarization_error_code
                                error_messages = NOS_API.test_cases_results_info.ber_vertical_polarization_error_message
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("Power on vertical polarization")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.power_vertical_polarization_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_vertical_polarization_error_message)
                            NOS_API.set_error_message("Tuner")
                            error_codes = NOS_API.test_cases_results_info.power_vertical_polarization_error_code
                            error_messages = NOS_API.test_cases_results_info.power_vertical_polarization_error_message
                            System_Failure = 2         
                    else:
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        System_Failure = 2
                else:
                    TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                        + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                    NOS_API.set_error_message("Video HDMI")
                    error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                    error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                    System_Failure = 2
        
    #####################################################################################################################################################################################################################################
    ####################################################################################################    HORIZONTAL    ###############################################################################################################
    ####################################################################################################   POLARIZATION   ###############################################################################################################
    #####################################################################################################################################################################################################################################
                
                if(test_result_ver):
                
                    ## Zap to horizontal polarization channel
                    TEST_CREATION_API.send_ir_rc_command(NOS_API.HORIZONTAL_POLARIZATION_CHANNEL_NUMBER)
                    
                    ## Perform grab picture
                    if (NOS_API.grab_picture("signal_menu_hor")):
                        
                        try:
                            ## Extract text from image
                            signal_strength_hor = NOS_API.replace_missed_chars_with_numbers(TEST_CREATION_API.OCR_recognize_text("signal_menu_hor", "[POWER_CANAIS_MENU]", "[OCR_FILTER]"))
                            TEST_CREATION_API.write_log_to_file("OCR: " + str(signal_strength_hor))
                            if not(NOS_API.represent_float(signal_strength_hor)):
                                signal_strength_hor = 17
                            else:
                                signal_strength_hor = float(signal_strength_hor)
                        
                            TEST_CREATION_API.write_log_to_file("Power horizontal polarization: " + str(signal_strength_hor) + "dBuV")
                            NOS_API.update_test_slot_comment("Power horizontal polarization: " + str(signal_strength_hor) + "dBuV")
                            NOS_API.test_cases_results_info.power_horizontal_polarization = str(signal_strength_hor)
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            signal_strength_hor = 17
                            NOS_API.test_cases_results_info.power_horizontal_polarization = "-"
                        
                        if(NOS_API.validate_threshold_range(signal_strength_hor, NOS_API.thresholds_info.power_horizontal) == True):
                            try:            
                                ber_hor = NOS_API.fix_ber(TEST_CREATION_API.OCR_recognize_text("signal_menu_hor", "[BER_CANAIS_MENU]", "[OCR_FILTER]"))
                                TEST_CREATION_API.write_log_to_file("BER horizontal polarization: " + ber_hor)
                                NOS_API.update_test_slot_comment("BER horizontal polarization: " + ber_hor)
                                NOS_API.test_cases_results_info.ber_horizontal_polarization = ber_hor
                                #ber_hor = float(ber_hor)
                                
                            except Exception as error:
                                ## Set test result to INCONCLUSIVE
                                ber_hor = "-"
                                NOS_API.test_cases_results_info.ber_horizontal_polarization = "-"
        
                            if(NOS_API.validate_threshold_range(ber_hor, NOS_API.thresholds_info.ber_horizontal, True) == True):
                                test_result = "PASS"
                                System_Failure = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("Ber on horizontal polarization")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.ber_horizontal_polarization_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.ber_horizontal_polarization_error_message)
                                NOS_API.set_error_message("Tuner")
                                error_codes = NOS_API.test_cases_results_info.ber_horizontal_polarization_error_code
                                error_messages = NOS_API.test_cases_results_info.ber_horizontal_polarization_error_message
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("Power on horizontal polarization")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.power_horizontal_polarization_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.power_horizontal_polarization_error_message)
                            NOS_API.set_error_message("Tuner")
                            error_codes = NOS_API.test_cases_results_info.power_horizontal_polarization_error_code
                            error_messages = NOS_API.test_cases_results_info.power_horizontal_polarization_error_message  
                            System_Failure = 2
                        
                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                    else:
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                                + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
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
                    "- - " + str(power_percentage) + " " + str(signal_quality_percentage) + " - - - " + NOS_API.test_cases_results_info.power_horizontal_polarization + " " + str(ber_hor) + " " + NOS_API.test_cases_results_info.power_vertical_polarization + " " + str(ber_hor) + " - " + str(logistic_serial_number) + " " + str(cas_id_number) + " " + str(firmware_version) + " " + str(nagra_guide_version) + " " + str(sc_number) + " - - - -",
                    "- - - - - - - - - " + str(NOS_API.thresholds_info.power_horizontal) + " " + str(NOS_API.thresholds_info.ber_horizontal) + " " + str(NOS_API.thresholds_info.power_vertical) + " " + str(NOS_API.thresholds_info.ber_vertical) + " " + str(NOS_API.thresholds_info.firmware_version) + " " + str(NOS_API.thresholds_info.nagraguide_version) + " - - - - -",
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

