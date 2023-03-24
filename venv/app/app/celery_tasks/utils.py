
def update_task_status(task):
    def inner_function(number, total):
        if number % 100 == 0:
            task.update_state(state='PROGRESS',
                              meta={'current': number, 'total': total})

    return inner_function