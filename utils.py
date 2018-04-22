import re


def month_to_number(name):
    months = {"Jan": "1",
              "Feb": "2",
              "Mar": "3",
              "Apr": "4",
              "May": "5",
              "June": "6",
              "July": "7",
              "Aug": "8",
              "Sept": "9",
              "Oct": "10",
              "Nov": "11",
              "Dec": "12"}

    return months[name].zfill(2)


def format_date(str_list, pos_day):
    return str_list[pos_day].zfill(2) + "." + month_to_number(str_list[pos_day - 1]) + "." + str_list[pos_day + 1].zfill(4)


# Example input: "(Apr.1, 2018)"
def format_date_album(arg):
    # extract date
    # ['', 'Apr', '1', '2018', '']
    tmp_list = re.split('\W+', arg)
    return format_date(tmp_list, 2)


# Example input: "2Y-10M-12Ds old (Apr.11, 2018)"
def format_date_file(arg):
    # extract date from round brackets
    # ['2Y', '10M', '12Ds', 'old', 'Apr', '11', '2018', '']
    tmp_list = re.split('\W+', arg)

    return format_date(tmp_list, -3)


# Example input: "(July.30, 2015) ·Family Members and Fans"
# use like so:
#   (date, acc) = format_date_access("(July.30, 2015) ·Family Members and Fans")
def format_date_access(arg):
    # extract date and access
    # ['', 'July', '30', '2015', 'Family', 'Members', 'and', 'Fans']
    tmp_list = re.split('\W+', arg)

    return format_date(tmp_list, 2), " ".join(tmp_list[4:])

    
def html_to_user_comment(str_arg):
    (tag1, tag2) = ("<mark>", "</mark>")
    start_usr = str_arg.index(tag1) + len(tag1)
    end_usr = str_arg.index(":")
    start_com = str_arg.index(tag2) + len(tag2)
    user = str_arg[start_usr:end_usr].replace("\n", " ").strip()
    comment = str_arg[start_com:].replace("\n", " ").strip()
    return (user, comment)
    
    
# parent:'1M old (June.30, 2015) · Family Members and Fans'
#  child:'1M old'
      
if __name__ == "__main__":
    print(format_date_album("(Apr.1, 2018)"))
    print(format_date_file("2Y-10M-12Ds old (Apr.11, 2018)"))
    (date, acc) = format_date_access("(July.30, 2015) ·Family Members and Fans")
    print(date)
    print(acc)
    
    test ="""
                <mark>Me :</mark>
                
                Liked this photo
                
              """
