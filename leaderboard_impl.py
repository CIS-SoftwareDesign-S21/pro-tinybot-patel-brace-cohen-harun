import discord
import json
import pandas as pd
import os

class leaderb:

    # Function to Display the Leaderboard
    def displayLeaderboard(ctx):

        # Open the JSON to be Loaded and Obtain Users
        with open("leaderboard2.json") as lb_file:
            lb_data = json.load(lb_file)
            print(lb_data)

        # Sort Leaderboards by Rank
        lb_info = pd.json_normalize(lb_data['users'])
#        print(lb_info)

        lb_info.sort_values(['wins'], axis = 0, ascending = False, inplace = True)
#        print(lb_info)

        # Close the JSON File
        lb_file.close()

        # Display the Leaderboards
        return lb_info


    # Function to Add a New User to the Leaderboard
    def addNewUser(ctx, userID, userName):

        print(userID)

        # Open the JSON to be Loaded
        with open("leaderboard2.json") as lb_file:
            lb_data = json.load(lb_file)
            print(lb_data)

        # Assure the User doesn't already Exist in the Leaderboard
        for i in lb_data['users']:
            print(i['user_id'])
            if int(i['user_id']) == userID:
                print("User Already Exists")
                return

        temp = lb_data['users']

        # Create User to Append to JSON File
        nUser = {"user_id": f"{userID}",
                 "user_name": f"{userName}",
                 "wins": 0,
                 "losses": 0
                }

        temp.append(nUser)

        # Append to JSON File
        with open("leaderboard2.json", 'w') as file:
            json.dump(lb_data, file, indent = 4)

        # Close the JSON File
        file.close()

        return

    # Function to Update the Leaderboards for Wins and Losses
    def updateLeaderboard(ctx, winner, loser, winnerName, loserName):

        # Add any New User(s) to the Leaderboard
        leaderb.addNewUser(ctx, winner, winnerName)
        leaderb.addNewUser(ctx, loser, loserName)

        # Open the JSON to be Loaded
        with open("leaderboard2.json") as lb_file:
            lb_data = json.load(lb_file)
            print(lb_data)

        for i in lb_data['users']:
            if int(i['user_id']) == winner:
                i['wins'] += 1
                if i['user_name'] != winnerName:
                    i['user_name'] = winnerName
            if int(i['user_id']) == loser:
                i['losses'] += 1
                if i['user_name'] != loserName:
                    i['user_name'] = loserName

        # For Testing Purposes
#        print(lb_data)

        with open("leaderboard2.json", 'w') as file:
            json.dump(lb_data, file, indent = 4)

        # Close the JSON File
        file.close()

        return
