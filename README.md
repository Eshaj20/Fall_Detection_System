#Fall_Detection_System
-----------------------------------------------------------------------
- Used Dataset : https://github.com/nhoyh/HR_IMU_falldetection_dataset
From the dataset we mainly included the 10 parameters which are ax, ay, az, w, x, y, z, droll, dpitch, dyaw.

Trained models :
- knn_model.pkl (binary classification)
- knn_model_all.pkl (multiclass classification)
  
We have evaluated with different machine learning techniques like catboost,xgboost,KNN and random forest such that we got a good accuracy in KNN which is around 96% using binary classification for fall detection and 92% using multiclass classification for activity recognition.Tested the sampled data by manually adding the data inputs into a platform of frontend(Reactjs) and backend(Flask).And also built a cross-platform mobile app (Android/iOS) using React Native with real-time fall alerts, SOS functionality, live location tracking, and emergency contact calling.

- Demo Video :  https://drive.google.com/file/d/1obMsI_Lfy0LN4a6dlX5d63ZHFQZnQksz/view?usp=drivesdk
