Created by Eric on May 29. 

====
Done
====

Trains correctly - change flag max_epoch for # epochs. 

Prints out images correctly. Only does it at the end. 

Doesn't save checkpoints correctly. Unsure why. 

Metrics are both printed and saved in error_file_{timestamp}.csv. Each row i of error_file = (training loss, test loss) at epoch i. 

====
Todo
====

Make loading work - likely bc I set the save_dir to model. However, actual checkpoints don't go in model, they just go in general directory. 