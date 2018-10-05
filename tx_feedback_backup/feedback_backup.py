import SqlService
import os
import shutil
from config import config


def feedback():
    feedback_list=SqlService.ct_feedback()
       
    for feedback_info in feedback_list:
        pid=feedback_info[0]
        feedback_type=feedback_info[1]
        backup_type=['DICOMS','output']
        for backup in backup_type:
            if not os.path.exists(feedback_path+feedback_type+'/'+pid+'/'+backup):
                if os.path.exists(dicom_path+pid):
                    shutil.copytree(dicom_path+pid,feedback_path+feedback_type+'/'+pid+'/'+backup)
		

if __name__ == '__main__':
    dicom_path=config.PATH.dicom_path
    output_path=config.PATH.output_path
    feedback_path=config.PATH.feedback_path
    for folder in ['miss','false']:
        if not os.path.exists(feedback_path+folder):
	    os.makedirs(feedback_path+folder)
    feedback()
