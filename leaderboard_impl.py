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

#            for i in lb_data['users']:
#                print(i['user_name'])

        # Sort Leaderboards by Rank
        lb_info = pd.json_normalize(lb_data['users'])
        print(lb_info)
#        print(pd.json_normalize(lb_data['users']))

        lb_info.sort_values(['wins'], axis = 0, ascending = True, inplace = True)
        print(lb_info)

        # Display the Leaderboards
        return lb_info


    # Function to Add a New User to the Leaderboard
    def addNewUser(ctx, userID):

        #### Insure User Doesn't already Exist ####

        # Open the JSON to be Loaded
        with open("leaderboard2.json") as lb_file:
            lb_data = json.load(lb_file)
            print(lb_data)

            temp = lb_data['users']

            # Create User to Append to JSON File
            nUser = {"user_name": f"{userID}",
                     "wins": "0",
                     "losses": "0"
                    }

            temp.append(nUser)

        # Append to JSON File
        with open("leaderboard2.json", 'w') as file:
            json.dump(lb_data, file, indent = 4)

        return

    # Function to Update the Leaderboards for Wins and Losses
    def updateLeaderboard(game, winner, loser):

        return
    
    # Update User's Name if it was changed since last played
    def namechangeLeaderboard(newID, oldID):

        #### MAY NOT NEED TO DO SINCE WERE USING USER ID'S WHICH DON'T CHANGE ####

        return
