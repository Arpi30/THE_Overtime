import time

def configure_progressbar(progressbar):
    num_of_steps = 100
    progressbar.set(0)
    progress_val = 1/num_of_steps
    step_val = 0
    for i in range(num_of_steps):
        step_val += progress_val
        progressbar.set(step_val)
        progressbar.update_idletasks()
        time.sleep(0.01)
    progressbar.destroy()