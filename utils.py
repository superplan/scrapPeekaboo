import re

# Example input: "2Y-10M-12Ds old (Apr.11, 2018)"
def format_date(arg):
    
    # extract date from round brackets
    # ['2Y', '10M', '12Ds', 'old', 'Apr', '11', '2018', '']
    tmp_list = re.split('\W+', arg)
    
    months = {  "Jan" : "1",
                "Feb" : "2",
                "Mar" : "3",
                "Apr" : "4",
                "May" : "5",
                "June" : "6",
                "July" : "7",
                "Aug." : "8",
                "Sept" : "9",
                "Oct" : "10",
                "Nov" : "11",
                "Dec" : "12" }
    
    return tmp_list[-3].zfill(2) + "." + months[tmp_list[-4]].zfill(2) + "." + tmp_list[-2].zfill(4)


# Example input: "(July.30, 2015) ·Family Members and Fans"
# use like so:
#   (date, acc) = format_date_access("(July.30, 2015) ·Family Members and Fans")
def format_date_access(arg):
    # extract date and access
    # ['', 'July', '30', '2015', 'Family', 'Members', 'and', 'Fans']
    tmp_list = re.split('\W+', arg)

    months = {"Jan": "1",
              "Feb": "2",
              "Mar": "3",
              "Apr": "4",
              "May": "5",
              "June": "6",
              "July": "7",
              "Aug.": "8",
              "Sept": "9",
              "Oct": "10",
              "Nov": "11",
              "Dec": "12"}

    return (tmp_list[2].zfill(2) + "." + months[tmp_list[1]].zfill(2) + "." + tmp_list[3].zfill(4), " ".join(tmp_list[4:]))