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
    def updateLeaderboard(game, winner, loser, winnerName, loserName):

        # Add any New User(s) to the Leaderboard
        addNewUser(winner, winnerName)
        addNewUser(loser, loserName)

        # Open the JSON to be Loaded
        with open("leaderboard2.json") as lb_file:
            lb_data = json.load(lb_file)
            print(lb_data)

        for i in lb_data['users']:
            if int(i['user_id']) == winner:
                i['wins'] += 1
            if int(i['user_id']) == loser:
                i['losses'] += 1

        # For Testing Purposes
#        print(lb_data)

        with open("leaderboard2.json", 'w') as file:
            json.dump(lb_data, file, indent = 4)

        # Close the JSON File
        file.close()

        return
    
    # Update User's Name if it was changed since last played
    def namechangeLeaderboard(newID, oldID):

        #### MAY NOT NEED TO DO SINCE WERE USING USER ID'S WHICH DON'T CHANGE ####

        return
