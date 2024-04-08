# 
#html_content="""
#    <!DOCTYPE html>
#    <html lang="en">
#    <head>
#        <title>Search Results for """+str(search_term)+""" </title>
#        <meta charset="UTF-8">
#        <meta http-equiv="X-UA-Compatible" content="IE=edge">
#        <meta name="viewport" content="width=device-width, initial-scale=1.0">
#        <style>
#        body, h1, h2, p, ul, li {
#            margin: 0;
#            padding: 0;
#        }
#        body {
#            font-family: Arial, sans-serif;
#            background-color: #f7f7f7;
#            color: #333;
#            display: flex;
#            flex-direction: column;
#            min-height: 100vh;
#        }
#        .heading {
#            font-size: 30px;
#            margin-bottom: 5px;
#            margin-left: auto;
#            margin-right: auto;
#            color:#000000;
#            font-family: sans-serif;
#            font-weight: bold;
#        }
#        .writtentext {
#            font-size: 16px;
#            margin-bottom: 2px;
#            color:#f7f7f7;
#            font-family: sans-serif;
#        }
#        .card-container{
#          display: flex;
#          flex-direction: column;
#          margin: 10px;
#          padding: 20px;
#        }
#        .card{
#          background-color: antiquewhite;
#          margin-right: 10px;
#          margin-left: 10px;
#          margin-bottom: 10px;
#          padding: 20px;
#          border-radius: 10px;
#          box-shadow: 2px 2px 2px 2px #000000;
#        }
#
#        .link-container{
#          display: flex;
#          flex-direction: column;
#          margin: 10px;
#          padding: 20px;
#        }
#
#        .list-links{
#            list-style-type: square;
#        }
#        .link-element{
#            margin: 10px 0;
#            padding: 20px;
#            border-radius: 10px;
#            box-shadow: 2px 2px 2px 2px #000000;
#            background-color: antiquewhite;
#            font-weight: bolder;
#        }
#        .card-heading{
#            margin: 0 auto;
#        }
#        .collapsible-list {
#            list-style-type: none;
#            margin: 0;
#            padding: 0;
#        }
#    .collapsible-content {
#    display: none;
#    background-color: antiquewhite; /* Background color similar to card */
#    margin: 10px;
#    padding: 20px;
#    border-radius: 10px;
#    box-shadow: 2px 2px 2px 2px #000000; 
#    }
#
#    .collapsible-button {
#    background-color: #eee;
#    color: #333;
#    cursor: pointer;
#    padding: 10px;
#    width: 100%;
#    text-align: left;
#    border: none;
#    outline: none; 
#    }
#
#   .collapsible-button:hover {
#    background-color: #ccc;
#    }
#
#    </style>
#    </head>
#    <body>
#        <div class="heading">
#            <p class="heading">Search Results for """ + str(search_term) +""" </p>
#        </div>
#                    <div class="card-container">
#    """
#    for res in search_results:
#        card_content=create_card_content(res)
#        html_content=html_content+'\n'+card_content
#    html_content=html_content+"""
#            </div>
#            <div class="link-container">
#                <div class="heading">
#                <p class="heading">
#                    We have also searched the Web for a few good links for you
#                </p>
#                </div>
#                <ul class="list-links">
#    """
#    for alink in dicoflinks:
#        linkcontent=f"""
#        <li class="link-element"><a href="{alink['href']}">{alink['name']}</a></li>
#        """
#        html_content=html_content+'\n'+linkcontent
#    html_content=html_content+"""
#                </ul>
#            </div>
#    <script>
#       function toggleCollapsible(event) {
#       var content = event.target.nextElementSibling;
#       content.style.display === 'none' ? content.style.display = 'block' : content.style.display = 'none';
#    }
#</script>
#    </body>
#</html>
#    """
#    #print(html_content)
#    output_file=f"{search_term}Results.html"
#    with open(output_file, 'w') as f:
#        f.write(html_content)
#    curr_dir=os.path.dirname(__file__)
#    file=os.path.join(curr_dir, output_file)
#    openfile='file:///'+file
#    webbrowser.open(openfile)