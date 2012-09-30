<html lang="en">
    <head>
        <meta charset="utf-8" /> 
        <title>Viddle</title>
        
        <link rel="stylesheet" href="/static/style.css" type="text/css" />
     </head>
     <body>
        <div id="container">
            <div id="header">
                <h1>Viddle</h1>
                <h2>Video search app</h2>
            </div>
            <div id="left_col">
                <div id="search">
                    <form action='search' method='get' accept-charset='utf-8'>\
                        <input type='text' name='term' value='' size='15' maxlength='30'/>\
                        <input type='submit' value='Search'/></p>\
                    </form>
                    <p class='supported'>Supported video sites: <b>tv.sme.sk</b>, <b>ted.com</b>, <b>sme.sk</b> (partially)</p>
                </div>
                
                <div id="results">
                    % if term != None:
                        <div>Searched term: <b>${term}</b></div><br>
                    % endif
                    
                    % if length == -1:
                        <p class='examples'>Examples of keywords: <b>matovič</b>, <b>internet</b>, <b>nikto</b>, <b>slovensky</b>...</p>
                    % elif length == 0:
                        <p class='error'>This search did not match any documents.</p>
                    % else:
                        <div><b>RESULTS: ${length}</b></div><br>
                    %    for item in data:
                             <div>
                                <a href="${item[0]}">${item[1]}</a><br>
                                <a href="${item[3]}">VIDEO</a> (score: ${item[2]})
                            </div>
                            <br>
                    %    endfor
                    % endif
                </div>
            </div>
            
            <div id="right_col">
                <h3>NEWEST</h3>
                <div id="newest">
                    % for item in newest:
                        <div>
                            <a href='${item[0]}'>${item[1]}</a><br>
                            <a href="${item[4]}">VIDEO</a> (${item[2]}, ${item[3]})
                        </div>
                        <br>
                    % endfor
                </div>
            </div>
        </div>
     </body>
</html>