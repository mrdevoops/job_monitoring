from kubernetes import client, config
from operator import itemgetter
import datetime

cron_job_name_list = ["cronjob1","cronjob2","cronjob3"]
namespace = 'namespace'
max_elapsed_time=5

def get_jobs(cron_job_name,jobs):
    jobs_list=[]
    for job in jobs.items:
        if cron_job_name in job.spec.template.metadata.labels['job-name']:
            jobs_list.append(job)   
    return jobs_list



def get_latest_job(jobs_list):
    job_start_time_list=[]
    for job in jobs_list:
        if job.status.start_time:
            job_start_time_list.append([job.status.start_time,job.metadata.uid])
    job_start_time_list=sorted(job_start_time_list,key=itemgetter(0),reverse=True)
    last_job=job_start_time_list[0]
    return last_job


def check_succsess_job(jobs_list,cron_shedule_time,cron_job_name):
    try:
        job_start_time,job_uid=get_latest_job(jobs_list)
    except IndexError:
        print ("No successful launches job found")
        return 1
    elapsed=job_start_time - cron_shedule_time
    if elapsed > datetime.timedelta(minutes=5):
        print ("Job fail to start in 5 minutes")
        return 1
    else:
        for job in jobs_list:
            if job.metadata.uid in job_uid:
                job_status=job.status.succeeded
                completion_time=job.status.completion_time
                if job_status!=1:
                    print ("Job fail to run with status" + job_status)
                    return 1
                else:
                    print (cron_job_name+" completed successfully at "+str(completion_time))
                    return 0

def load_metrics():
    #For local testing use kube_config
    #config.load_kube_config()
    config.load_incluster_config()
    batch_v1 = client.BatchV1Api()
    batch_v1beta1 = client.BatchV1beta1Api()
    status_cronjobs={}

    for cron_job_name in cron_job_name_list: 
        cron_job = batch_v1beta1.read_namespaced_cron_job(cron_job_name, namespace)
        jobs = batch_v1.list_namespaced_job(namespace)
        cron_shedule_time=cron_job.status.last_schedule_time
        jobs_list=get_jobs(cron_job_name,jobs)
        status_cronjobs[cron_job_name]=check_succsess_job(jobs_list,cron_shedule_time,cron_job_name)
    return status_cronjobs,namespace
