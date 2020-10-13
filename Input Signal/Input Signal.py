# Test name = Input Signal
# Test description = Check signal strength

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

THRESHOLD = 60

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

            ## Initialize grabber device
            NOS_API.initialize_grabber()

            ## Start grabber device with video on default video source
            NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
            time.sleep(1)
            
            if (NOS_API.is_signal_present_on_video_source()):
            
                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if (video_height != "720"):
                    ## Set resolution to 720p
                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p]")
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height != "720"):
                        if not(NOS_API.grab_picture("Check_Resolucao")):
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
                        TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                        TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_720p]")
                        
                        if not(NOS_API.grab_picture("Check_Resolucao_2")):
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
                        
                        if (video_height != "720"):
                            NOS_API.set_error_message("Resolução")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                            error_codes = NOS_API.test_cases_results_info.resolution_error_code
                            error_messages = NOS_API.test_cases_results_info.resolution_error_message
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
                            
                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
            
                if (NOS_API.test_cases_results_info.channel_boot_up_state):

                    TEST_CREATION_API.send_ir_rc_command("[IMAGE_ZON]")  
                    if not(NOS_API.grab_picture("Check_English")):
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
                    if (TEST_CREATION_API.compare_pictures("English_Menu_ref", "Check_English", "[Check_English]")):
                        TEST_CREATION_API.send_ir_rc_command("[Change_Language]")
                        if not(NOS_API.grab_picture("Check_Portuguese")):
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
                        if not(TEST_CREATION_API.compare_pictures("zon_box_ref", "Check_Portuguese", "[SETTINGS]")):
                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                            TEST_CREATION_API.send_ir_rc_command("[IMAGE_ZON]") 
                            TEST_CREATION_API.send_ir_rc_command("[Change_Language]")
                            if not(NOS_API.grab_picture("Check_Portuguese_1")):
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
                            if not(TEST_CREATION_API.compare_pictures("zon_box_ref", "Check_Portuguese_1", "[SETTINGS]")):
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
                    TEST_CREATION_API.send_ir_rc_command("[SIGNAL_LEVEL_SETTINGS]")
                    if (NOS_API.grab_picture("signal_value")):
                        if not(TEST_CREATION_API.compare_pictures("signal_value_ref", "signal_value", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref_old", "signal_value", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "signal_value", "[SIGNAL_VALUE_MENU]")):
                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                            TEST_CREATION_API.send_ir_rc_command("[IMAGE_ZON]")    
                            TEST_CREATION_API.send_ir_rc_command("[SIGNAL_LEVEL_SETTINGS]")
                            
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
                            if not(TEST_CREATION_API.compare_pictures("signal_value_ref", "signal_value", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref_old", "signal_value", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "signal_value", "[SIGNAL_VALUE_MENU]")):
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
                        
                        macro_signal_level = "[SIGNAL_VALUE_50_PERCENT]"
                        macro_signal_quality = "[SIGNAL_QUALITY_50_PERCENT]"
                        ref_image = "signal_value_ref"              
     
                        try:
                            signal_value = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_level)
                            signal_quality = NOS_API.compare_pictures(ref_image, "signal_value", macro_signal_quality)
                        
                        except Exception as error:
                            ## Set test result to INCONCLUSIVE
                            TEST_CREATION_API.write_log_to_file(str(error))
                            signal_value = 0
                            signal_quality = 0
                            
                        ## Check if signal value higher than threshold                        
                        if (signal_value >= THRESHOLD and signal_quality >= THRESHOLD):
                            #test_result = "PASS" 
                            TEST_CREATION_API.send_ir_rc_command("[OK]")
                            result = NOS_API.wait_for_multiple_pictures(["Installed_Channels_ref", "Installed_Channels_ref1"], 25, ["[Sic]", "[Sic]"], [80, 80])
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
                                result_2 = NOS_API.wait_for_multiple_pictures(["new_sw_detected_message_720", "Check_Nagra_ref"], 15, ["[SW_UPGRADE_MESSAGE_720]", "[Nagra_Upgrade]"], [NOS_API.thres, NOS_API.thres])
                                if (result_2 == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
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
                                if (result_2 == -1):
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    time.sleep(5)
                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                    result_2 = NOS_API.wait_for_multiple_pictures(["new_sw_detected_message_720", "Check_Nagra_ref"], 15, ["[SW_UPGRADE_MESSAGE_720]", "[Nagra_Upgrade]"], [NOS_API.thres, NOS_API.thres])
                                if (result_2 == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
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
                                if (result_2 == 0):
                                    result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_started_via_ota", "sw_upgrade_started_via_ota_ref1"], 30, ["[WRITE_SW_HDMI]", "[WRITE_SW_HDMI]"], [NOS_API.thres, NOS_API.thres])
                                    if (result != -1 and result != -2):
                                        result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_progress_ref", "sw_upgrade_progress_ref1"], 400, ["[WRITE_SW_HDMI]", "[WRITE_SW_HDMI]"], [NOS_API.thres, NOS_API.thres])
                                        if (result != -1 and result != -2):                            
                                            if (NOS_API.wait_for_no_signal_present(90)):
                                                NOS_API.test_cases_results_info.DidUpgrade = 1
                                                if not(NOS_API.wait_for_signal_present(25)):
                                                    TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                time.sleep(15)
                                                NOS_API.test_cases_results_info.channel_boot_up_state = True
                                                test_result = "PASS"
                                                result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref", "Check_Nagra_1080_ref"], 35, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [NOS_API.thres, NOS_API.thres])
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
                                                    video_result = 0
                                                    while(video_result == 0):
                                                        time.sleep(2)
                                                        video_result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref", "Check_Nagra_1080_ref"], 5, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [NOS_API.thres, NOS_API.thres])
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
                                            TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                            NOS_API.set_error_message("Não Actualiza")
                                            error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                            error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message 
                                            System_Failure = 2
                                elif (result_2 == 1):
                                    while(video_result == 0):
                                        time.sleep(2)
                                        video_result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref", "Check_Nagra_1080_ref"], 5, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [NOS_API.thres, NOS_API.thres])
                                    test_result = "PASS"
                                    System_Failure = 2
                                else:
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                                    TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                                    result_2 = NOS_API.wait_for_multiple_pictures(["menu_720_ref", "menu_720_new_ref", "menu_720_new_ref1"], 25, ["[MENU_720]", "[MENU_NEW_720]", "[MENU_NEW_720]"], [70, 70, 70])
                                    if (result_2 == 0 or result_2 == 1 or result_2 == 2):                               
                                        test_result = "PASS"
                                        System_Failure = 2
                                    else:
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
                                TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                                TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                                result_2 = NOS_API.wait_for_multiple_pictures(["menu_720_ref", "menu_720_new_ref", "menu_720_new_ref1"], 25, ["[MENU_720]", "[MENU_NEW_720]", "[MENU_NEW_720]"], [70, 70, 70])
                                if (result_2 == 0 or result_2 == 1 or result_2 == 2):                               
                                    test_result = "PASS"
                                    System_Failure = 2
                                else:                            
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
                            if not(NOS_API.grab_picture("Check_Parameters")):
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
                            if (TEST_CREATION_API.compare_pictures("Signal_Parameters_ref", "Check_Parameters", "[Signal_Parameters_Channel]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "Check_Parameters", "[Signal_Parameters_Channel]")):
                                TEST_CREATION_API.send_ir_rc_command("[Change_Signal_Parameters]")
                                if not(NOS_API.grab_picture("signal_value_2")):
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
                                signal_value = NOS_API.compare_pictures(ref_image, "signal_value_2", macro_signal_level)
                                signal_quality = NOS_API.compare_pictures(ref_image, "signal_value_2", macro_signal_quality)
                            
                            except Exception as error:
                                ## Set test result to INCONCLUSIVE
                                TEST_CREATION_API.write_log_to_file(str(error))
                                signal_value = 0
                                signal_quality = 0
                                
                            ## Check if signal value higher than threshold                        
                            if (signal_value >= THRESHOLD and signal_quality >= THRESHOLD):
                                TEST_CREATION_API.send_ir_rc_command("[OK]")
                                result = NOS_API.wait_for_multiple_pictures(["Installed_Channels_ref", "Installed_Channels_ref"], 25, ["[Sic]", "[Sic]"], [80, 80])
                                if (result == -2):
                                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
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
                                if (result != -1):
                                    TEST_CREATION_API.send_ir_rc_command("[OK]")
                                    result_2 = NOS_API.wait_for_multiple_pictures(["new_sw_detected_message_720", "Check_Nagra_ref"], 25, ["[SW_UPGRADE_MESSAGE_720]", "[Nagra_Upgrade]"], [NOS_API.thres, NOS_API.thres])
                                    if (result_2 == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
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
                                    if (result_2 == -1):
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        time.sleep(5)
                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                        result_2 = NOS_API.wait_for_multiple_pictures(["new_sw_detected_message_720", "Check_Nagra_ref"], 15, ["[SW_UPGRADE_MESSAGE_720]", "[Nagra_Upgrade]"], [NOS_API.thres, NOS_API.thres])
                                    if (result_2 == -2):
                                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
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
                                    if (result_2 == 0):
                                        result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_started_via_ota", "sw_upgrade_started_via_ota_ref1"], 30, ["[WRITE_SW_HDMI]", "[WRITE_SW_HDMI]"], [NOS_API.thres, NOS_API.thres])
                                        if (result != -1 and result != -2):
                                            result = NOS_API.wait_for_multiple_pictures(["sw_upgrade_progress_ref", "sw_upgrade_progress_ref1"], 400, ["[WRITE_SW_HDMI]", "[WRITE_SW_HDMI]"], [NOS_API.thres, NOS_API.thres])
                                            if (result != -1 and result != -2):                            
                                                if (NOS_API.wait_for_no_signal_present(90)):
                                                    NOS_API.test_cases_results_info.DidUpgrade = 1
                                                    if not(NOS_API.wait_for_signal_present(25)):
                                                        TEST_CREATION_API.send_ir_rc_command("[POWER]")
                                                    time.sleep(15)
                                                    NOS_API.test_cases_results_info.channel_boot_up_state = True
                                                    test_result = "PASS"
                                                    result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref", "Check_Nagra_1080_ref"], 35, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [NOS_API.thres, NOS_API.thres])
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
                                                        video_result = 0
                                                        while(video_result == 0):
                                                            time.sleep(2)
                                                            video_result = NOS_API.wait_for_multiple_pictures(["Check_Nagra_ref", "Check_Nagra_1080_ref"], 5, ["[FULL_SCREEN]", "[FULL_SCREEN]"], [NOS_API.thres, NOS_API.thres])
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
                                                TEST_CREATION_API.write_log_to_file("Doesn't upgrade")
                                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.upgrade_nok_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.upgrade_nok_error_message)
                                                NOS_API.set_error_message("Não Actualiza")
                                                error_codes = NOS_API.test_cases_results_info.upgrade_nok_error_code
                                                error_messages = NOS_API.test_cases_results_info.upgrade_nok_error_message
                                                System_Failure = 2                                                
                                    elif (result_2 == 1):
                                        NOS_API.test_cases_results_info.DidUpgrade = 1
                                        time.sleep(120)
                                        test_result = "PASS"
                                        System_Failure = 2
                                    else:
                                        TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                                        TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                                        result_2 = NOS_API.wait_for_multiple_pictures(["menu_720_ref", "menu_720_new_ref", "menu_720_new_ref1"], 25, ["[MENU_720]", "[MENU_NEW_720]", "[MENU_NEW_720]"], [70, 70, 70])
                                        if (result_2 == 0 or result_2 == 1 or result_2 == 2):                               
                                            test_result = "PASS"
                                            System_Failure = 2
                                        else:
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
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                                    TEST_CREATION_API.send_ir_rc_command("[MENU_1]")
                                    result_2 = NOS_API.wait_for_multiple_pictures(["menu_720_ref", "menu_720_new_ref", "menu_720_new_ref1"], 25, ["[MENU_720]", "[MENU_NEW_720]", "[MENU_NEW_720]"], [70, 70, 70])
                                    if (result_2 == 0 or result_2 == 1 or result_2 == 2):
                                        TEST_CREATION_API.send_ir_rc_command("[IMAGE_ZON]")
                                        TEST_CREATION_API.send_ir_rc_command("[SIGNAL_LEVEL_SETTINGS]")
                                        if not(NOS_API.grab_picture("Right_Place")):
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
                                        if not(TEST_CREATION_API.compare_pictures("signal_value_ref", "Right_Place", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref_old", "Right_Place", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "Right_Place", "[SIGNAL_VALUE_MENU]")):
                                            TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                                            TEST_CREATION_API.send_ir_rc_command("[IMAGE_ZON]")    
                                            TEST_CREATION_API.send_ir_rc_command("[SIGNAL_LEVEL_SETTINGS]")
                                            
                                            if not(NOS_API.grab_picture("Right_Place")):
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
                                            if not(TEST_CREATION_API.compare_pictures("signal_value_ref", "Right_Place", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref_old", "Right_Place", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "Right_Place", "[SIGNAL_VALUE_MENU]")):
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
                                        test_result = "PASS"
                                        System_Failure = 2
                                    else:                            
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
                                NOS_API.display_dialog("Confirme o cabo RF e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                time.sleep(1)
                                
                                if not(NOS_API.grab_picture("signal_value_4")):
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
                                
                                if not(TEST_CREATION_API.compare_pictures("signal_value_ref", "signal_value_4", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref_old", "signal_value_4", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "signal_value_4", "[SIGNAL_VALUE_MENU]")):
                                    if not(NOS_API.grab_picture("signal_value_3")):
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
                                    TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                                    TEST_CREATION_API.send_ir_rc_command("[IMAGE_ZON]")    
                                    TEST_CREATION_API.send_ir_rc_command("[SIGNAL_LEVEL_SETTINGS]")
                                    
                                    if not(NOS_API.grab_picture("signal_value_4")):
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
                                    if not(TEST_CREATION_API.compare_pictures("signal_value_ref", "signal_value_4", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref_old", "signal_value_4", "[SIGNAL_VALUE_MENU]") or TEST_CREATION_API.compare_pictures("signal_value_ref1", "signal_value_4", "[SIGNAL_VALUE_MENU]")):
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
                                    signal_value = NOS_API.compare_pictures(ref_image, "signal_value_4", macro_signal_level)
                                    signal_quality = NOS_API.compare_pictures(ref_image, "signal_value_4", macro_signal_quality)
                                
                                except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    signal_value = 0
                                    signal_quality = 0
                                
                                ## Check if signal value higher than threshold                        
                                if (signal_value >= THRESHOLD and signal_quality >= THRESHOLD):
                                    test_result = "PASS"
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
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        NOS_API.set_error_message("Video HDMI")
                        System_Failure = 2
                else:
                    test_result = "PASS"
                    System_Failure = 2
                        
            else:
                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                       + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                NOS_API.set_error_message("Video HDMI")
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