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
                    <%!
                        import re
                            
                        def is_youtube(text):
                            return re.match(r"^http://www.youtube.com", text)
                            
                        def is_tvsme(text):
                            return re.match(r"^http://i.sme.sk/datamm", text)
                            
                        def parse_tvsme_video_id(text):
                            return re.findall(r"[0-9]{5}", text)[0]
                            
                        def is_ted(text):
                            return re.match(r"^http://video.ted.com", text);
                    %>
                         
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
                                <a href="${item[0]}">${item[1]}</a>  (score: ${item[2]})
                                % if is_youtube(item[3]):
                                    <iframe width="400" height="300" src="${item[3]}" frameborder="0" allowfullscreen=""></iframe>
                                % elif is_ted(item[3]):
                                    <embed 
                                        src="http://video.ted.com/assets/player/swf/EmbedPlayer.swf" 
                                        pluginspace="http://www.macromedia.com/go/getflashplayer" 
                                        type="application/x-shockwave-flash"
                                        wmode="transparent" 
                                        bgColor="#ffffff" 
                                        width="400" 
                                        height="300"
                                        allowFullScreen="true" 
                                        allowScriptAccess="always" 
                                        flashvars="vu=${item[3]}&vw=385&amp;vh=215">
                                    </embed>
                                % elif is_tvsme(item[3]):
                                <%
                                    video_id = parse_tvsme_video_id(item[3])
                                %>
                                    <iframe width="400" height="300" border="0" frameborder="0" scrolling="no" style="padding:0px; margin:0px; border: 0px;" src="http://www.sme.sk/vp/${video_id}/"></iframe>
                                % else:
                                    <video width="400" height="300" controls>
                                        <source src="${item[3]}" type='video/mp4' />
                                        Your browser does not support the video tag.
                                    </video>
                                % endif
                            </div>
                    %    endfor
                    % endif
                </div>
            </div>
            
            <div id="right_col">
                <h3>NEWEST</h3>
                <div id="newest">
                    % for item in newest:
                        <div>
                            <a href='${item[0]}'>${item[1]}</a> (${item[2]} ${item[3]})<br>
                        </div>
                        <br>
                    % endfor
                </div>
            </div>
        </div>
     </body>
</html>