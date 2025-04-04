from django.shortcuts import render
import joblib
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Load the trained models
linear_regressor = joblib.load('total_percentage_model.pkl')
logistic_regressor = joblib.load('pass_fail_model.pkl')

# Index and other views
def index(request):
    return render(request, 'index.html')

def student(request):
    return render(request, 'student.html')


def student_dashboard(request):
    if request.method == 'POST':
        # Helper function to safely convert form input to float
        def safe_float(value):
            try:
                return float(value)
            except (TypeError, ValueError):
                return 0.0  # Return a default value if conversion fails

        # Capture form data with default value handling
        student_data = {
            'Name': request.POST.get('name'),
            'Study Hours per Day': safe_float(request.POST.get('study_Hours')),
            'Stress Level': safe_float(request.POST.get('stress_Level')),
            'Test 1': {
                'English': safe_float(request.POST.get('english1')),
                'Maths': safe_float(request.POST.get('maths1')),
                'Science': safe_float(request.POST.get('science1')),
                'Hindi': safe_float(request.POST.get('hindi1')),
                'Computer': safe_float(request.POST.get('computer1'))
            },
            'Test 2': {
                'English': safe_float(request.POST.get('english2')),
                'Maths': safe_float(request.POST.get('maths2')),
                'Science': safe_float(request.POST.get('science2')),
                'Hindi': safe_float(request.POST.get('hindi2')),
                'Computer': safe_float(request.POST.get('computer2'))
            },
            'Test 3': {
                'English': safe_float(request.POST.get('english3')),
                'Maths': safe_float(request.POST.get('maths3')),
                'Science': safe_float(request.POST.get('science3')),
                'Hindi': safe_float(request.POST.get('hindi3')),
                'Computer': safe_float(request.POST.get('computer3'))
            },
            'Test 4': {
                'English': safe_float(request.POST.get('english4')),
                'Maths': safe_float(request.POST.get('maths4')),
                'Science': safe_float(request.POST.get('science4')),
                'Hindi': safe_float(request.POST.get('hindi4')),
                'Computer': safe_float(request.POST.get('computer4'))
            },
            'Test 5': {
                'English': safe_float(request.POST.get('english5')),
                'Maths': safe_float(request.POST.get('maths5')),
                'Science': safe_float(request.POST.get('science5')),
                'Hindi': safe_float(request.POST.get('hindi5')),
                'Computer': safe_float(request.POST.get('computer5'))
            },
            'Attendance': {
                'English': safe_float(request.POST.get('englishAttendance')),
                'Maths': safe_float(request.POST.get('mathsAttendance')),
                'Science': safe_float(request.POST.get('scienceAttendance')),
                'Hindi': safe_float(request.POST.get('hindiAttendance')),
                'Computer': safe_float(request.POST.get('computerAttendance'))
            },
            'Class Average': {
                'English': safe_float(request.POST.get('englishAvg')),
                'Maths': safe_float(request.POST.get('mathsAvg')),
                'Science': safe_float(request.POST.get('scienceAvg')),
                'Hindi': safe_float(request.POST.get('hindiAvg')),
                'Computer': safe_float(request.POST.get('computerAvg'))
            },
            'Goal Score': {
                'English': safe_float(request.POST.get('englishGoal')),
                'Maths': safe_float(request.POST.get('mathsGoal')),
                'Science': safe_float(request.POST.get('scienceGoal')),
                'Hindi': safe_float(request.POST.get('hindiGoal')),
                'Computer': safe_float(request.POST.get('computerGoal'))
            }
        }

        # Initialize variables for totals and averages
        totalAttendance = 0

        totalEnglishAverage = 0
        totalMathsAverage = 0
        totalScienceAverage = 0
        totalHindiAverage = 0
        totalComputerAverage = 0

        test1_Total = 0
        test2_Total = 0
        test3_Total = 0
        test4_Total = 0
        test5_Total = 0

        # Calculate the total attendance
        for subject in student_data['Attendance']:
            totalAttendance += student_data['Attendance'][subject]

        # Calculate the total marks for each test and averages for each subject
        for test_num in range(1, 6):
            test_key = f'Test {test_num}'
            test_scores = student_data[test_key]
            
            # Add the test total for each test
            for subject in test_scores:
                if test_num == 1:
                    test1_Total += test_scores[subject]
                elif test_num == 2:
                    test2_Total += test_scores[subject]
                elif test_num == 3:
                    test3_Total += test_scores[subject]
                elif test_num == 4:
                    test4_Total += test_scores[subject]
                elif test_num == 5:
                    test5_Total += test_scores[subject]
                
                # Calculate averages for each subject
                if subject == 'English':
                    totalEnglishAverage += test_scores[subject]
                elif subject == 'Maths':
                    totalMathsAverage += test_scores[subject]
                elif subject == 'Science':
                    totalScienceAverage += test_scores[subject]
                elif subject == 'Hindi':
                    totalHindiAverage += test_scores[subject]
                elif subject == 'Computer':
                    totalComputerAverage += test_scores[subject]


        # Below code is written for when user give only 1, 2.. test // for per subject 

        if(test3_Total == 0 and test4_Total ==0 and test5_Total == 0):
            totalEnglishAverage /= 2
            totalMathsAverage /= 2
            totalScienceAverage /= 2
            totalHindiAverage /= 2
            totalComputerAverage /= 2
        elif(test4_Total ==0 and test5_Total == 0):
            totalEnglishAverage /= 3
            totalMathsAverage /= 3
            totalScienceAverage /= 3
            totalHindiAverage /= 3
            totalComputerAverage /= 3
        elif(test5_Total == 0):
            totalEnglishAverage /= 4
            totalMathsAverage /= 4
            totalScienceAverage /= 4
            totalHindiAverage /= 4
            totalComputerAverage /= 4
        else :
            totalEnglishAverage /= 5
            totalMathsAverage /= 5
            totalScienceAverage /= 5
            totalHindiAverage /= 5
            totalComputerAverage /= 5

        # Divide totalAttendance by the number of subjects (assuming 5 subjects)
        totalAttendance /= 5
        
        # Below code is written for when user give only 1, 2.. test  // for per test
        total_percentage = 0
        if(test2_Total == 0 and test3_Total ==0 and test4_Total == 0 and test5_Total ==0 ):
            total_percentage = test1_Total / 5
        elif(test3_Total == 0 and test4_Total ==0 and test5_Total == 0):
            total_percentage = (test1_Total + test2_Total) / 10
        elif(test4_Total ==0 and test5_Total == 0):
            total_percentage = (test1_Total + test2_Total + test3_Total) / 15
        elif(test5_Total == 0):
            total_percentage = (test1_Total + test2_Total + test3_Total + test4_Total) / 20
        else :
            total_percentage = (test1_Total + test2_Total + test3_Total + test4_Total + test5_Total) / 25

        # Prepare input for model prediction using form data
        X_input = np.array([[totalAttendance, 
                             student_data['Study Hours per Day'], 
                             student_data['Stress Level'],total_percentage]])

   
        # Predict Total Percentage using the linear regression model
        Pred_total_percentage = linear_regressor.predict(X_input)[0]
        
        # Predict Pass/Fail using the logistic regression model
        pass_fail = logistic_regressor.predict(X_input)[0]

        # Predict Pass/Fail probabilities
        pass_fail_probabilities = logistic_regressor.predict_proba(X_input)[0]  # Get probabilities for both classes

        # Extract Pass/Fail probabilities
        pass_probability = pass_fail_probabilities[1]  # Probability of passing (class 1)
        fail_probability = pass_fail_probabilities[0]  # Probability of failing (class 0)


        # Recommendation System --------------------------------------------------------------------------

        df = pd.read_csv('subjects_images_dataset.csv')

        english_books = []
        hindi_books= []
        maths_books=[]
        science_books=[]
        computer_books=[]

        if(totalEnglishAverage>=60) :
            english_books = df.iloc[[0, 1, 2], [1]].values.flatten().tolist()
        elif(totalEnglishAverage>=45):
            english_books = df.iloc[[3, 4, 5], [1]].values.flatten().tolist()
        elif(totalEnglishAverage<45):
            english_books = df.iloc[[7, 8, 9], [1]].values.flatten().tolist()

        if(totalHindiAverage>=60) :
            hindi_books = df.iloc[[0, 1, 2], [2]].values.flatten().tolist()
        elif(totalEnglishAverage>=45):
            hindi_books = df.iloc[[3, 4, 5], [2]].values.flatten().tolist()
        elif(totalEnglishAverage<45):
            hindi_books = df.iloc[[7, 8, 9], [2]].values.flatten().tolist()

        if(totalMathsAverage>=60) :
            maths_books = df.iloc[[0, 1, 2], [3]].values.flatten().tolist()
        elif(totalEnglishAverage>=45):
            maths_books = df.iloc[[3, 4, 5], [3]].values.flatten().tolist()
        elif(totalEnglishAverage<45):
            maths_books = df.iloc[[7, 8, 9], [3]].values.flatten().tolist()

        if(totalScienceAverage>=60) :
            science_books = df.iloc[[0, 1, 2], [4]].values.flatten().tolist()
        elif(totalEnglishAverage>=45):
            science_books = df.iloc[[3, 4, 5], [4]].values.flatten().tolist()
        elif(totalEnglishAverage<45):
            science_books = df.iloc[[7, 8, 9], [4]].values.flatten().tolist()

        if(totalComputerAverage>=60) :
            computer_books = df.iloc[[0, 1, 2], [5]].values.flatten().tolist()
        elif(totalEnglishAverage>=45):
            computer_books = df.iloc[[3, 4, 5], [5]].values.flatten().tolist()
        elif(totalEnglishAverage<45):
            computer_books = df.iloc[[7, 8, 9], [5]].values.flatten().tolist()

        english_resources = {
            "Books" : english_books,
            "YouTube": [
                "https://www.youtube.com/channel/UCyDXMl-ru1F--NPCtO7aDig",
                "https://www.youtube.com/user/bbclearningenglish"
            ],
            "Websites": [
                "https://www.bbc.co.uk/learningenglish",
                "https://www.duolingo.com/"
            ],
            "Courses": [
                "https://www.coursera.org/learn/careerdevelopment"
            ]
        }

        hindi_resources = {
            "Books" : hindi_books,
            "YouTube": [
                "https://www.youtube.com/@MagnetBrainsEducation",
                "https://www.youtube.com/@Class10HindiMedium"
            ],
            "Websites": [
                "https://nitin-gupta.com/most-important-general-hindi-notes/#google_vignette",
                "https://study91.co.in/"
            ],
            "Courses": [
                "https://www.udemy.com/topic/hindi/?srsltid=AfmBOopqyGCltYibfEjs58I5XShy1O1h6FKsbD-8ywv4meq1LFjhlskS"
            ]
        }

        maths_resources = {
            "Books" : maths_books,
            "YouTube": [
                "https://www.youtube.com/@MariosMathTutoringr",
                "https://www.youtube.com/c/numberphile"
            ],
            "Websites": [
                "https://www.khanacademy.org/",
                "https://www.brilliant.org/"
            ],
            "Courses": [
                "https://www.coursera.org/learn/mathematical-thinking"
            ]
        }

        science_resources = {
            "Books" : science_books,
            "YouTube": [
                "https://www.youtube.com/c/ScienceChannel",
                "https://www.youtube.com/c/AsapSCIENCE"
            ],
            "Websites": [
                "https://www.khanacademy.org/",
                "https://education.nationalgeographic.org/"
            ],
            "Courses": [
                "https://www.edx.org/course/introduction-to-biology-the-secret-of-life"
            ]
        }

        computer_resources = {
            "Books" : computer_books,
            "YouTube": [
                "https://www.youtube.com/@freecodecamp",
                "https://www.youtube.com/c/TheNetNinja"
            ],
            "Websites": [
                "https://www.codecademy.com/",
                "https://www.freecodecamp.org/"
            ],
            "Courses": [
                "https://www.coursera.org/specializations/introduction-computer-science-programming"
            ]
        }


        # Prepare data to send to the template
        context = {
            'Name': student_data['Name'],
            'totalAttendance': totalAttendance,
            'totalEnglishAverage': totalEnglishAverage,
            'totalMathsAverage': totalMathsAverage,
            'totalScienceAverage': totalScienceAverage,
            'totalHindiAverage': totalHindiAverage,
            'totalComputerAverage': totalComputerAverage,

            'test1_Total': test1_Total / 5,
            'test2_Total': test2_Total / 5,
            'test3_Total': test3_Total / 5,
            'test4_Total': test4_Total / 5,
            'test5_Total': test5_Total / 5,

            'english_class_avg': student_data['Class Average']['English'],
            'maths_class_avg': student_data['Class Average']['Maths'],
            'hindi_class_avg': student_data['Class Average']['Hindi'],
            'science_class_avg': student_data['Class Average']['Science'],
            'computer_class_avg': student_data['Class Average']['Computer'],


            'english_attendance': student_data['Attendance']['English'],
            'maths_attendance': student_data['Attendance']['Maths'],
            'hindi_attendance': student_data['Attendance']['Hindi'],
            'science_attendance': student_data['Attendance']['Science'],
            'computer_attendance': student_data['Attendance']['Computer'],

            'english_Goal': student_data['Goal Score']['English'],
            'maths_Goal': student_data['Goal Score']['Maths'],
            'hindi_Goal': student_data['Goal Score']['Hindi'],
            'science_Goal': student_data['Goal Score']['Science'],
            'computer_Goal': student_data['Goal Score']['Computer'],

            'total_percentage': Pred_total_percentage,
            'pass_fail': 'Pass' if pass_fail == 1 else 'Fail',
            'pass_probability': round(pass_probability * 100, 2),  # Convert to percentage
            'fail_probability': round(fail_probability * 100, 2),  # Convert to percentage

            'english_resources' : english_resources,
            'hindi_resources' : hindi_resources,
            'maths_resources' : maths_resources,
            'science_resources' : science_resources,
            'computer_resources' : computer_resources,

       }

        return render(request, 'student_dashboard.html', context)
    else:
        # Handle GET request (if needed)
        return render(request, 'student_dashboard.html')





# def student_dashboard(request):
#     # Dummy data for now
#     student_data = {
#         'Attendance Percentage': 80,
#         'Study Hours per Day': 5,
#         'Stress Level': 3
#     }

#     # Prepare input for model prediction using dummy data
#     X_input = np.array([[student_data['Attendance Percentage'], student_data['Study Hours per Day'], student_data['Stress Level']]])

#     # Predict Total Percentage using the linear regression model
#     total_percentage = linear_regressor.predict(X_input)[0]
    
#     # Predict Pass/Fail using the logistic regression model
#     pass_fail = logistic_regressor.predict(X_input)[0]

#     # Predict Pass/Fail probabilities
#     pass_fail_probabilities = logistic_regressor.predict_proba(X_input)[0]  # Get probabilities for both classes

#     # Extract Pass/Fail probabilities
#     pass_probability = pass_fail_probabilities[1]  # Probability of passing (class 1)
#     fail_probability = pass_fail_probabilities[0]  # Probability of failing (class 0)

#     # Prepare data to send to the template
#     context = {
#         'total_percentage': total_percentage,
#         'pass_fail': 'Pass' if pass_fail == 1 else 'Fail',
#         'pass_probability': round(pass_probability * 100, 2),  # Convert to percentage
#         'fail_probability': round(fail_probability * 100, 2),  # Convert to percentage
#         'student_data': student_data  # Send dummy student data to the template
#     }
#     return render(request, 'student_dashboard.html', context)

# Educator view
def educator(request):
    return render(request, 'educator.html')

def educator_dashboard(request):
    return render(request, 'educator_dashboard.html')

# @csrf_exempt
# def predict_student_performance(request):
#     if request.method == 'POST':
#         # Input data from the user (can be from a form or JSON)
#         data = json.loads(request.body)
#         attendance = data['Attendance Percentage']
#         study_hours = data['Study Hours per Day']
#         stress_level = data['Stress Level']
        
#         # Prepare input for model prediction
#         X_input = np.array([[attendance, study_hours, stress_level]])

#         # Predict Total Percentage using the linear regression model
#         total_percentage = linear_regressor.predict(X_input)[0]
        
#         # Predict Pass/Fail using the logistic regression model
#         pass_fail = logistic_regressor.predict(X_input)[0]
        
#         # Predict Pass/Fail probabilities
#         pass_fail_probabilities = logistic_regressor.predict_proba(X_input)[0]
        
#         # Extract Pass/Fail probabilities
#         pass_probability = pass_fail_probabilities[1]  # Probability of passing (class 1)
#         fail_probability = pass_fail_probabilities[0]  # Probability of failing (class 0)

#         # Return results as a JSON response
#         response_data = {
#             'Total Percentage': total_percentage,
#             'Pass/Fail': 'Pass' if pass_fail == 1 else 'Fail',
#             'Pass Probability': round(pass_probability * 100, 2),  # Return as percentage
#             'Fail Probability': round(fail_probability * 100, 2)   # Return as percentage
#         }
#         return JsonResponse(response_data)

#     return JsonResponse({'error': 'Invalid request'}, status=400)
