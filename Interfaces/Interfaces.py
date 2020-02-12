# -*- coding: utf-8 -*-
# Test name = Zap Test
# Test description = Check image and audio after channel up/channel down

from datetime import datetime
from time import gmtime, strftime
import time

import TEST_CREATION_API
#import shutil
#shutil.copyfile('\\\\bbtfs\\RT-Executor\\API\\NOS_API.py', 'NOS_API.py')
import NOS_API

## Max record audio time in miliseconds
MAX_RECORD_AUDIO_TIME = 2000

MAX_RECORD_VIDEO_TIME = 2000

def runTest():

    ## Skip this test case if some of previous tests from test plan failed
    if not(NOS_API.test_cases_results_info.isTestOK):
        TEST_CREATION_API.update_test_result(TEST_CREATION_API.TestCaseResult.FAIL)        
        return
    
    System_Failure = 0
    
    while (System_Failure < 2):  
        try:
            if(System_Failure == 1):
                ## Initialize grabber device
                NOS_API.initialize_grabber()

                ## Start grabber device with video on default video source
                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)   
            
                TEST_CREATION_API.send_ir_rc_command("[EXIT_ZON_BOX]")
                TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
                TEST_CREATION_API.send_ir_rc_command("[EXIT_1]")
        
                if not(NOS_API.is_signal_present_on_video_source()):
                    TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                    NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                            + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                    NOS_API.set_error_message("Reboot")
                    error_codes = NOS_API.test_cases_results_info.reboot_error_code
                    error_messages = NOS_API.test_cases_results_info.reboot_error_message
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
                
            ## Set test result default to FAIL
            test_result = "FAIL"
            pqm_analyse_check = True
            
            Zap_test_result = False
            HDMI1080_test_result = False
            Composite_test_result = False
            test_result_res = False
            
            error_codes = ""
            error_messages = ""

            chUp_counter = 0
            chDown_counter = 0
            
            if(System_Failure == 0):
                ## Initialize grabber device
                NOS_API.initialize_grabber()

                ## Start grabber device with video on default video source
                NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.HDMI1)
                TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.HDMI1)       
            
            if not(NOS_API.is_signal_present_on_video_source()):
                time.sleep(5)
            
            if (NOS_API.is_signal_present_on_video_source()):            

            #####################################################################################################################################################################################################################################
    ###################################################################################################       Zap        ###############################################################################################################
    ###################################################################################################      Test        ###############################################################################################################
    ##################################################################################################################################################################################################################################### 
                ## Zap to service
                TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                
                ## Set volume to max
                TEST_CREATION_API.send_ir_rc_command("[VOL_MIN]")
                
                ## Set volume to half, because if vol is max, signal goes in saturation
                TEST_CREATION_API.send_ir_rc_command("[VOL_PLUS_HALF]")

                while (chUp_counter < 3):
                    video_result = 0
            
                    ## Close info banner
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    
                    result = NOS_API.wait_for_multiple_pictures(["Black_HDMI_ref"], 5, ["[FULL_SCREEN]"], [80])
                    if (result != -1 and result != -2):
                        TEST_CREATION_API.send_ir_rc_command("[CH_3]")
                        time.sleep(3)
                        TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                        
                    try:
                        ## Perform grab picture
                        TEST_CREATION_API.grab_picture("service_2")

                        video_result = NOS_API.compare_pictures("service_2_ref", "service_2", "[HALF_SCREEN]")
            
                    except Exception as error:
                        ## Set test result to INCONCLUSIVE
                        TEST_CREATION_API.write_log_to_file(str(error))
                        test_result = "FAIL"
                        TEST_CREATION_API.write_log_to_file("There is no signal on HDMI interface.")        
            
                    ## Record audio from HDMI
                    TEST_CREATION_API.record_audio("audio_chUp", MAX_RECORD_AUDIO_TIME)
            
                    ################################################################################################ Amostras de som OK##################################################################################################
                    #
                    #audio_result_1 = NOS_API.compare_audio("audio_chUp_ref1", "audio_chUp")
                    #audio_result_2 = NOS_API.compare_audio("audio_chUp_ref2", "audio_chUp")
                    #
                    ### Check if STB zap to horizontal polarization channel (check image and audio)
                    #if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD)):
                    #    
                    #    NOS_API.test_cases_results_info.chUp_state = True
                    #    break
                    #else:
                    #    if (chUp_counter == 2):
                    #        if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                    #            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                    #            NOS_API.set_error_message("Audio HDMI")
                    #            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                    #                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                    #                                            + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                    #                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                    #            error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                    #            error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                    #        else:                       
                    #            TEST_CREATION_API.write_log_to_file("STB is not zap to service 2 (ChUp failed)")
                    #            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.zap_channel_up_error_code \
                    #                                                + "; Error message: " + NOS_API.test_cases_results_info.zap_channel_up_error_message \
                    #                                                + "; V: " + str(video_result))
                    #            NOS_API.set_error_message("Tuner")
                    #            error_codes = NOS_API.test_cases_results_info.zap_channel_up_error_code
                    #            error_messages = NOS_API.test_cases_results_info.zap_channel_up_error_message
                    #    else:
                    #        TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                    #        time.sleep(3)
                    #        TEST_CREATION_API.send_ir_rc_command("[CH-]")
                    #        time.sleep(3)
                    #        TEST_CREATION_API.send_ir_rc_command("[CH+]")
                    #chUp_counter = chUp_counter + 1
                    ######################################################################################################################################################################################################################
                     
                    audio_result_1 = NOS_API.compare_audio("No_Both_ref", "audio_chUp") 
                    if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD)):
                        
                        NOS_API.test_cases_results_info.chUp_state = True
                        break
                    else:
                        if (chUp_counter == 2):
                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                NOS_API.set_error_message("Audio HDMI")
                                NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                System_Failure = 2
                            else:                       
                                TEST_CREATION_API.write_log_to_file("STB is not zap to service 2 (ChUp failed)")
                                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.zap_channel_up_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.zap_channel_up_error_message \
                                                                    + "; V: " + str(video_result))
                                NOS_API.set_error_message("Tuner")
                                error_codes = NOS_API.test_cases_results_info.zap_channel_up_error_code
                                error_messages = NOS_API.test_cases_results_info.zap_channel_up_error_message
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.send_ir_rc_command("[CH_3]")
                            time.sleep(4)
                            TEST_CREATION_API.send_ir_rc_command("[CH_4]")
                            time.sleep(5)
                            #TEST_CREATION_API.send_ir_rc_command("[CH-]")
                            #time.sleep(3)
                            #TEST_CREATION_API.send_ir_rc_command("[CH+]")
                    chUp_counter = chUp_counter + 1
                    
                ###################
                ## CH Down
                ###################
                if (NOS_API.test_cases_results_info.chUp_state == True):
                    
                    ## Zap to service
                    TEST_CREATION_API.send_ir_rc_command(NOS_API.CHANNEL)
                    time.sleep(1)
                    
                    if not (NOS_API.is_signal_present_on_video_source()):
                        TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                        NOS_API.set_error_message("Reboot")
                        error_codes = NOS_API.test_cases_results_info.reboot_error_code
                        error_messages = NOS_API.test_cases_results_info.reboot_error_message
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
                    
                    result = NOS_API.wait_for_multiple_pictures(["Black_HDMI_ref"], 5, ["[FULL_SCREEN]"], [80])
                    if (result != -1 and result != -2):
                        if not(NOS_API.grab_picture("Black_Screnn")):
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
                         
                        TEST_CREATION_API.send_ir_rc_command("[CH_3]")
                        time.sleep(3)
                        TEST_CREATION_API.send_ir_rc_command("[CH-]")
                        time.sleep(3)
                        TEST_CREATION_API.send_ir_rc_command("[CH+]")
                        
                        result = NOS_API.wait_for_multiple_pictures(["Black_HDMI_ref"], 5, ["[FULL_SCREEN]"], [80])
                        if (result != -1 and result != -2):
                            
                            time.sleep(5)
                            
                            if not(NOS_API.grab_picture("Black_Screnn_1")):
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
                               
                    ## Record video with duration of recording (10 seconds)
                    NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                
                    ## Instance of PQMAnalyse type
                    pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                
                    ## Set what algorithms should be checked while analyzing given video file with PQM.
                    # Attributes are set to false by default.
                    pqm_analyse.black_screen_activ = True
                    pqm_analyse.blocking_activ = True
                    pqm_analyse.freezing_activ = True
                
                    # Name of the video file that will be analysed by PQM.
                    pqm_analyse.file_name = "video"
                
                    ## Analyse recorded video
                    analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                
                    if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message)
                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_code
                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_absence_error_message
                
                    if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message)
                                
                        if (error_codes == ""):
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                        else:
                            error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_code
                        
                        if (error_messages == ""):
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                        else:
                            error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_blocking_error_message
                    
                    if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                        pqm_analyse_check = False
                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code \
                                + "; Error message: " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message)
                                
                        if (error_codes == ""):
                            error_codes = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                        else:
                            error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_code
                            
                        if (error_messages == ""):
                            error_messages = NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                        else:
                            error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_720p_image_freezing_error_message
                                                     
                    if not(pqm_analyse_check): 
                        NOS_API.set_error_message("Video HDMI")
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
                                          
                        return
                    
                    if not(analysed_video):
                        if(System_Failure == 0):
                            System_Failure = System_Failure + 1 
                            NOS_API.Inspection = True
                            if(System_Failure == 1):
                                try:
                                    ## Return DUT to initial state and de-initialize grabber device
                                    NOS_API.deinitialize()
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
                                continue
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
                            TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                            error_codes = NOS_API.test_cases_results_info.grabber_error_code
                            error_messages = NOS_API.test_cases_results_info.grabber_error_message
                            NOS_API.set_error_message("Inspection")
                            
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
                            
                            return
                       
                    ## Check if video is playing (check if video is not freezed)
                    if (NOS_API.is_video_playing()):

                        while (chDown_counter < 3):
                            video_result = 0          
                
                            ## Close info banner
                            TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                
                            try:
                                    ## Perform grab picture
                                TEST_CREATION_API.grab_picture("service_1")
                
                                video_result = NOS_API.compare_pictures("service_1_ref", "service_1", "[HALF_SCREEN]")
                
                            except Exception as error:
                                    ## Set test result to INCONCLUSIVE
                                    TEST_CREATION_API.write_log_to_file(str(error))
                                    test_result = "FAIL"
                                    TEST_CREATION_API.write_log_to_file("There is no signal on HDMI interface.")
                
                            ## Record audio from HDMI
                            TEST_CREATION_API.record_audio("audio_chDown", MAX_RECORD_AUDIO_TIME)
                            
                            ################################################################################################ Amostras de som OK##################################################################################################
                            #
                            #audio_result_1 = NOS_API.compare_audio("audio_chDown_ref1", "audio_chDown")
                            #audio_result_2 = NOS_API.compare_audio("audio_chDown_ref2", "audio_chDown")
                            #
                            ### Check if STB zap to channel (check image and audio)
                            #if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD)):
                            #    
                            #    #test_result = "PASS"
                            #    Zap_test_result = True
                            #    break
                            #else:
                            #    if (chDown_counter == 2):
                            #        if(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                            #            TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                            #            NOS_API.set_error_message("Audio HDMI")
                            #            NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                            #                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                            #                                            + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                            #                                            + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                            #            error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                            #            error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                            #        else:
                            #            TEST_CREATION_API.write_log_to_file("STB is not zap to service 1")
                            #            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.zap_channel_down_error_code \
                            #                                                + "; Error message: " + NOS_API.test_cases_results_info.zap_channel_down_error_message \
                            #                                                + "; V: " + str(video_result))
                            #            NOS_API.set_error_message("Tuner")
                            #            error_codes = NOS_API.test_cases_results_info.zap_channel_down_error_code
                            #            error_messages = NOS_API.test_cases_results_info.zap_channel_down_error_message
                            #    else:
                            #        TEST_CREATION_API.send_ir_rc_command(NOS_API.CHANNEL)
                            #        TEST_CREATION_API.send_ir_rc_command("[CH+]")
                            #        time.sleep(2)
                            #        TEST_CREATION_API.send_ir_rc_command("[CH-]")
                            #chDown_counter = chDown_counter + 1
                            #########################################################################################################################################################################################################################
                            
                            audio_result_1 = NOS_API.compare_audio("No_Both_ref", "audio_chDown")
                            
                            if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD and (audio_result_1 < TEST_CREATION_API.AUDIO_THRESHOLD)):
                                
                                #test_result = "PASS"
                                Zap_test_result = True
                                break
                            else:
                                if (chDown_counter == 2):
                                    if(video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on hdmi 720p interface.")
                                        NOS_API.set_error_message("Audio HDMI")
                                        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code  \
                                                                        + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code  \
                                                                        + "; Error messages: " + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message \
                                                                        + ";\n" + NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message)
                                        error_codes = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_code
                                        error_messages = NOS_API.test_cases_results_info.hdmi_720p_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.hdmi_720p_signal_interference_error_message
                                        System_Failure = 2
                                    else:
                                        TEST_CREATION_API.write_log_to_file("STB is not zap to service 1")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.zap_channel_down_error_code \
                                                                            + "; Error message: " + NOS_API.test_cases_results_info.zap_channel_down_error_message \
                                                                            + "; V: " + str(video_result))
                                        NOS_API.set_error_message("Tuner")
                                        error_codes = NOS_API.test_cases_results_info.zap_channel_down_error_code
                                        error_messages = NOS_API.test_cases_results_info.zap_channel_down_error_message
                                        System_Failure = 2
                                else:
                                    TEST_CREATION_API.send_ir_rc_command(NOS_API.CHANNEL)
                                    TEST_CREATION_API.send_ir_rc_command("[CH+]")
                                    time.sleep(2)
                                    TEST_CREATION_API.send_ir_rc_command("[CH-]")
                            chDown_counter = chDown_counter + 1
                            
            else:
                TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                       + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                NOS_API.set_error_message("Video HDMI")
                error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                System_Failure = 2
                
    #####################################################################################################################################################################################################################################
    ###################################################################################################        SET        ###############################################################################################################
    ################################################################################################### Resolution(1080p) ###############################################################################################################
    #####################################################################################################################################################################################################################################            
                
            if(Zap_test_result):
            
                TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080p]")
                time.sleep(2)
        
                video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                if (video_height != "1080"):
                    TEST_CREATION_API.send_ir_rc_command("[SET_RESOLUTION_1080p]")
                    time.sleep(2)
                    video_height = NOS_API.get_av_format_info(TEST_CREATION_API.AudioVideoInfoType.video_height)
                    if (video_height != "1080"):
                        NOS_API.set_error_message("Resolução")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.resolution_error_code \
                                                + "; Error message: " + NOS_API.test_cases_results_info.resolution_error_message) 
                        error_codes = NOS_API.test_cases_results_info.resolution_error_code
                        error_messages = NOS_API.test_cases_results_info.resolution_error_message
                        System_Failure = 2
                    else:
                        test_result_res = True
                else:
                    test_result_res = True
        
    #####################################################################################################################################################################################################################################
    ###################################################################################################       Video       ###############################################################################################################
    ###################################################################################################     HDMI(1080p)   ###############################################################################################################
    #####################################################################################################################################################################################################################################                
                        
                if(test_result_res):
                
                    pqm_analyse_check = True
                    
                    TEST_CREATION_API.send_ir_rc_command("[Left]")
                    TEST_CREATION_API.send_ir_rc_command("[Left]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    TEST_CREATION_API.send_ir_rc_command("[EXIT]")
                    
                    if not(NOS_API.is_signal_present_on_video_source()):
                        time.sleep(10)
                    if (NOS_API.is_signal_present_on_video_source()):
                        ## Record video with duration of recording (10 seconds)
                        NOS_API.record_video("video", MAX_RECORD_VIDEO_TIME)
                    
                        ## Instance of PQMAnalyse type
                        pqm_analyse = TEST_CREATION_API.PQMAnalyse()
                    
                        ## Set what algorithms should be checked while analyzing given video file with PQM.
                        # Attributes are set to false by default.
                        pqm_analyse.black_screen_activ = True
                        pqm_analyse.blocking_activ = True
                        pqm_analyse.freezing_activ = True
                    
                        # Name of the video file that will be analysed by PQM.
                        pqm_analyse.file_name = "video"
                    
                        ## Analyse recorded video
                        analysed_video = TEST_CREATION_API.pqm_analysis(pqm_analyse)
                    
                        if (pqm_analyse.black_screen_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message)
                                    
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_absence_error_message
                    
                        if (pqm_analyse.blocking_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message)
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_code
                            
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_blocking_error_message
                        
                        if (pqm_analyse.freezing_detected == TEST_CREATION_API.AlgorythmResult.DETECTED):
                            pqm_analyse_check = False
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                            if (error_codes == ""):
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                            else:
                                error_codes = error_codes + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                                
                            if (error_messages == ""):
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                            else:
                                error_messages = error_messages + " " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                        
                        if not(pqm_analyse_check): 
                            NOS_API.set_error_message("Video HDMI")
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
                                            
                            return
                        
                        if not(analysed_video):
                            if(System_Failure == 0):
                                System_Failure = System_Failure + 1 
                                NOS_API.Inspection = True
                                if(System_Failure == 1):
                                    try:
                                        ## Return DUT to initial state and de-initialize grabber device
                                        NOS_API.deinitialize()
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
                                    continue
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
                                TEST_CREATION_API.write_log_to_file("Could'n't Record Video")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.grabber_error_code \
                                                                                    + "; Error message: " + NOS_API.test_cases_results_info.grabber_error_message)
                                error_codes = NOS_API.test_cases_results_info.grabber_error_code
                                error_messages = NOS_API.test_cases_results_info.grabber_error_message
                                NOS_API.set_error_message("Inspection")
                                
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
                                
                                return              
                        
                        if not(NOS_API.is_signal_present_on_video_source):
                            TEST_CREATION_API.write_log_to_file("STB lost Signal.Possible Reboot.")
                            NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.reboot_error_code \
                                                    + "; Error message: " + NOS_API.test_cases_results_info.reboot_error_message)
                            NOS_API.set_error_message("Reboot")
                            error_codes = NOS_API.test_cases_results_info.reboot_error_code
                            error_messages = NOS_API.test_cases_results_info.reboot_error_message
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
                        ## Check if video is playing (check if video is not freezed)
                        if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.HDMI1, NOS_API.ResolutionType.resolution_1080p)):
                    
                            video_result = 0
                            i = 0
                            
                            while(i < 3):
                    
                                try:
                                    ## Perform grab picture
                                    TEST_CREATION_API.grab_picture("HDMI_video")
                            
                                    ## Compare grabbed and expected image and get result of comparison
                                    video_result = NOS_API.compare_pictures("HDMI_video_ref", "HDMI_video", "[HALF_SCREEN_1080p]")
                            
                                except:
                                    i = i + 1
                                    continue
                            
                                ## Check video analysis results and update comments
                                if (video_result >= TEST_CREATION_API.DEFAULT_HDMI_VIDEO_THRESHOLD):
                                    i = 0
                                    if (analysed_video): 
                                        HDMI1080_test_result = True
                                        #test_result = "PASS"
                                    else:
                                        NOS_API.set_error_message("Video HDMI")     
                                    break
                                i = i + 1
                            if (i >= 3):
                                TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly on HDMI 1080p.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message \
                                                                    + "; V: " + str(video_result))
                                error_codes = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_code
                                error_messages = NOS_API.test_cases_results_info.hdmi_1080p_noise_error_message
                                NOS_API.set_error_message("Video HDMI")
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing on HDMI 1080p.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message)
                            error_codes = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_code
                            error_messages = NOS_API.test_cases_results_info.hdmi_1080p_image_freezing_error_message
                            NOS_API.set_error_message("Video HDMI")
                            System_Failure = 2
                    else:
                        TEST_CREATION_API.write_log_to_file("Image is not displayed on HDMI")
                        NOS_API.update_test_slot_comment("Error code = " + NOS_API.test_cases_results_info.image_absence_hdmi_error_code \
                                                            + "; Error message: " + NOS_API.test_cases_results_info.image_absence_hdmi_error_message)
                        NOS_API.set_error_message("Video HDMI")
                        error_codes = NOS_API.test_cases_results_info.image_absence_hdmi_error_code
                        error_messages = NOS_API.test_cases_results_info.image_absence_hdmi_error_message
                        System_Failure = 2

    #######################################################################################################################################################################################################################################
    ###################################################################################################      Composite      ###############################################################################################################
    ###################################################################################################        Video        ###############################################################################################################
    #######################################################################################################################################################################################################################################                    
                    
                    if(HDMI1080_test_result):    
                        NOS_API.grabber_stop_video_source()
                        time.sleep(1)
                        NOS_API.grabber_stop_audio_source()
                        time.sleep(1)
                        
                        ## Initialize input interfaces of DUT RT-AV101 device 
                        NOS_API.reset_dut(TEST_CREATION_API.VideoInterface.CVBS)
                        
                        NOS_API.grabber_start_video_source(TEST_CREATION_API.VideoInterface.CVBS)
                        
                        if not(NOS_API.is_signal_present_on_video_source()):
                            NOS_API.display_dialog("Confirme o cabo de Video Composto e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                        
                        if (NOS_API.is_signal_present_on_video_source()):
                
                            ## Check if video is playing (check if video is not freezed)
                            if (NOS_API.is_video_playing(TEST_CREATION_API.VideoInterface.CVBS)):
                                video_result = 0
                                i = 0
                                
                                while(i < 3):
                    
                                    try:
                                        ## Perform grab picture
                                        TEST_CREATION_API.grab_picture("COMPOSITE_video")
                                
                                        ## Compare grabbed and expected image and get result of comparison
                                        video_result = NOS_API.compare_pictures("COMPOSITE_video_ref", "COMPOSITE_video", "[HALF_SCREEN_576p]")
                                
                                    except:
                                        i = i + 1
                                        continue
                
                                    ## Check video analysis results and update comments
                                    if (video_result >= NOS_API.DEFAULT_CVBS_VIDEO_THRESHOLD):
                                        ## Set test result to PASS
                                        Composite_test_result = True
                                        #test_result = "PASS"
                                        break
                                    i = i + 1
                                if (i == 1):
                                    NOS_API.display_dialog("Confirme o cabo de Video Composto e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"
                                if (i >= 3):
                                    TEST_CREATION_API.write_log_to_file("Video with RT-RK pattern is not reproduced correctly.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.composite_noise_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.composite_noise_error_message \
                                                                    + "; V: " + str(video_result))
                                    NOS_API.set_error_message("Video Composto")
                                    error_codes = NOS_API.test_cases_results_info.composite_noise_error_code
                                    error_messages = NOS_API.test_cases_results_info.composite_noise_error_message  
                                    System_Failure = 2
                            else:
                                TEST_CREATION_API.write_log_to_file("Channel with RT-RK color bar pattern was not playing.")
                                NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.composite_image_freezing_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.composite_image_freezing_error_message \
                                                                    + "; Video is not playing on COMPOSITE interface")
                                NOS_API.set_error_message("Video Composto")
                                error_codes = NOS_API.test_cases_results_info.composite_image_freezing_error_code
                                error_messages = NOS_API.test_cases_results_info.composite_image_freezing_error_message
                                System_Failure = 2
                        else:
                            TEST_CREATION_API.write_log_to_file("No video on Composite.")
                            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.composite_image_absence_error_code \
                                                                    + "; Error message: " + NOS_API.test_cases_results_info.composite_image_absence_error_message)
                            NOS_API.set_error_message("Video Composto")
                            error_codes = NOS_API.test_cases_results_info.composite_image_absence_error_code
                            error_messages = NOS_API.test_cases_results_info.composite_image_absence_error_message
                            System_Failure = 2
                            
    #######################################################################################################################################################################################################################################
    ###################################################################################################      Analogue       ###############################################################################################################
    ###################################################################################################        Audio        ###############################################################################################################
    #######################################################################################################################################################################################################################################
                        if(Composite_test_result):
                            NOS_API.grabber_stop_video_source()
                            time.sleep(1)
                            
                            ## Start grabber device with audio on analog audio source
                            TEST_CREATION_API.grabber_start_audio_source(TEST_CREATION_API.AudioInterface.LINEIN)
                            time.sleep(1.5)                            
                            
                            ## Due to artifact on analog audio, volume is decreased one time
                            TEST_CREATION_API.send_ir_rc_command("[VOL-]")
                            time.sleep(1)
                    
                            ## Record audio from analog output
                            TEST_CREATION_API.record_audio("analog_audio", MAX_RECORD_AUDIO_TIME)
                    
                            ################################################################################################ Amostras de som OK##################################################################################################                        
                            ### Compare recorded and expected audio and get result of comparison                    
                            #audio_result = NOS_API.compare_audio("analog_audio_ref", "analog_audio", "[AUDIO_ANALOG]")
                            #
                            #if (audio_result < TEST_CREATION_API.AUDIO_THRESHOLD):
                            #
                            #    NOS_API.display_dialog("Confirme os cabos de Audio Analogico e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"        
                            #
                            #    ## Record audio from analog output
                            #    TEST_CREATION_API.record_audio("analog_audio", MAX_RECORD_AUDIO_TIME)
                            #
                            ### Compare recorded and expected audio and get result of comparison
                            #
                            #audio_result = NOS_API.compare_audio("analog_audio_ref", "analog_audio", "[AUDIO_ANALOG]")
                            #
                            #
                            #if (audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            #
                            #    ## Check is audio present on channel
                            #    if (TEST_CREATION_API.is_audio_present("analog_audio")):
                            #        test_result = "PASS"
                            #        
                            #    else:
                            #        TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                            #        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                            #                                            + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message)
                            #        error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                            #        error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                            #        NOS_API.set_error_message("Audio Analogico")
                            #else:
                            #    time.sleep(3)
                            #    
                            #    ## Record audio from analog output
                            #    TEST_CREATION_API.record_audio("analog_audio1", MAX_RECORD_AUDIO_TIME)
                            #
                            #    ## Compare recorded and expected audio and get result of comparison
                            #    audio_result = NOS_API.compare_audio("analog_audio_ref", "analog_audio1", "[AUDIO_ANALOG]")
                            #
                            #    #if (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            #    if (audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            #
                            #        ## Check is audio present on channel
                            #        if (TEST_CREATION_API.is_audio_present("analog_audio1")):
                            #            test_result = "PASS"
                            #            
                            #        else:
                            #            TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                            #            NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                            #                                                    + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message)
                            #            error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                            #            error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                            #            NOS_API.set_error_message("Audio Analogico")
                            #    else:                    
                            #        TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on analog interface.")
                            #        NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code  \
                            #                                                    + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code  \
                            #                                                    + "; Error messages: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message \
                            #                                                    + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message)
                            #        error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code
                            #        error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message
                            #        NOS_API.set_error_message("Audio Analogico")
                            #        
                            #TEST_CREATION_API.send_ir_rc_command("[VOL+]")
                            ######################################################################################################################################################################################################################
                            
                            ## Compare recorded and expected audio and get result of comparison                    
                            audio_result = NOS_API.compare_audio("No_Left_Analogue_ref", "analog_audio", "[AUDIO_ANALOG]")
                            audio_result1 = NOS_API.compare_audio("No_Right_Analogue_ref", "analog_audio", "[AUDIO_ANALOG]")
                            audio_result2 = NOS_API.compare_audio("No_Both_Analogue_ref", "analog_audio", "[AUDIO_ANALOG]")
                            
                            if (audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            
                                NOS_API.display_dialog("Confirme os cabos de Audio Analogico e restantes cabos", NOS_API.WAIT_TIME_TO_CLOSE_DIALOG) == "Continuar"        
                            
                                ## Record audio from analog output
                                TEST_CREATION_API.record_audio("analog_audio", MAX_RECORD_AUDIO_TIME)
                            
                            ## Compare recorded and expected audio and get result of comparison
                            
                            audio_result = NOS_API.compare_audio("No_Left_Analogue_ref", "analog_audio", "[AUDIO_ANALOG]")
                            audio_result1 = NOS_API.compare_audio("No_Right_Analogue_ref", "analog_audio", "[AUDIO_ANALOG]")
                            audio_result2 = NOS_API.compare_audio("No_Both_Analogue_ref", "analog_audio", "[AUDIO_ANALOG]")                    
                            
                            if not(audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            
                                ## Check is audio present on channel
                                if (TEST_CREATION_API.is_audio_present("analog_audio")):
                                    test_result = "PASS"                               
                                else:
                                    TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                                    NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                                                                        + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message)
                                    error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                                    error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                                    NOS_API.set_error_message("Audio Analogico")
                                    System_Failure = 2
                            else:
                                time.sleep(3)
                                
                                ## Record audio from analog output
                                TEST_CREATION_API.record_audio("analog_audio1", MAX_RECORD_AUDIO_TIME)
                            
                                ## Compare recorded and expected audio and get result of comparison
                                audio_result = NOS_API.compare_audio("No_Left_Analogue_ref", "analog_audio1", "[AUDIO_ANALOG]")
                                audio_result1 = NOS_API.compare_audio("No_Right_Analogue_ref", "analog_audio1", "[AUDIO_ANALOG]")
                                audio_result2 = NOS_API.compare_audio("No_Both_Analogue_ref", "analog_audio1", "[AUDIO_ANALOG]")
                            
                                #if (audio_result_1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result_2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                                if not(audio_result >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result1 >= TEST_CREATION_API.AUDIO_THRESHOLD or audio_result2 >= TEST_CREATION_API.AUDIO_THRESHOLD):
                            
                                    ## Check is audio present on channel
                                    if (TEST_CREATION_API.is_audio_present("analog_audio1")):
                                        test_result = "PASS"
                                    else:
                                        TEST_CREATION_API.write_log_to_file("Audio is not present on analog interface.")
                                        NOS_API.update_test_slot_comment("Error code: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code \
                                                                                + "; Error message: " + NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message)
                                        error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_code
                                        error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_absence_error_message
                                        NOS_API.set_error_message("Audio Analogico")
                                        System_Failure = 2
                                else:                    
                                    TEST_CREATION_API.write_log_to_file("Audio with RT-RK pattern is not reproduced correctly on analog interface.")
                                    NOS_API.update_test_slot_comment("Error codes: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code  \
                                                                                + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code  \
                                                                                + "; Error messages: " + NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message \
                                                                                + ";\n" + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message)
                                    error_codes = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_code + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_code
                                    error_messages = NOS_API.test_cases_results_info.analogue_audio_signal_discontinuities_error_message + " " + NOS_API.test_cases_results_info.analogue_audio_signal_interference_error_message
                                    NOS_API.set_error_message("Audio Analogico")
                                    System_Failure = 2
                                    
                            TEST_CREATION_API.send_ir_rc_command("[VOL+]")
            
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