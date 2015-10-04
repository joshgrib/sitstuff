renderTable();

var timeblocks;
var courselist_arr;

function renderTable()
{
    timeblocks = [];
    var scheduleTable = document.getElementById("scheduleTable");scheduleTable.className = "schedule";
    // 8:00 through 21:00 is all we care about since no classes run earlier/later
    for(var i = 8; i < 21; i++)
    {
        var timeblock = document.createElement("tbody");
        timeblock.className = "timeblock-no";
        var hour = i % 12;
        hour = hour ? hour : 12;
        timeblocks[i] = timeblock;
        for(var mins = 0; mins < 60; mins += 15)
        {
            var timeblock_row = document.createElement("tr");
            if(mins == 0) // since the header rowspans by 4, you only need one of these to cover all four slots
            {
                var timeblock_row_header = document.createElement("td");
                timeblock_row_header.className = "time";
                timeblock_row_header.rowSpan = 4;
                timeblock_row_header.innerHTML = hour + ":00";
                timeblock_row.appendChild(timeblock_row_header);
                timeblock_row.className = "first-child";
            }

            for(var day = 0; day < 7; day++)
            {
                var timeblock_row_day = document.createElement("td");
                timeblock_row_day.className = "Day" + day;
                timeblock_row.appendChild(timeblock_row_day);
            }

            timeblock.appendChild(timeblock_row);
        }
        scheduleTable.appendChild(timeblock);
    }
}

var req;
// set up the AJAX object
// branch for native XMLHttpRequest object
if (window.XMLHttpRequest) {
    req = new XMLHttpRequest();
    // branch for IE/Windows ActiveX version
    } else if (window.ActiveXObject) {
    req = new ActiveXObject("Microsoft.XMLHTTP");
}

document.getElementById("termlist").onchange = termChange;
document.getElementById("courselist").onchange = courseChange;

function courseChange()
{
    var courseselect = document.getElementById('courselist');
    // destroy all unsaved classes
    DestroyUnsaved();
    var courseinfo = courseselect.options[courseselect.selectedIndex]['courseinfo'];
    var new_course = new Course(courseinfo);
    new_course.Render();
}

function processCourseReqChange()
{
    var courseselect = document.getElementById('courselist');
    var loadingbox = document.getElementById('loadingbox');

    if(req.readyState == 4)
    {
        if(req.status == 200)
        {
            var response = req.responseXML.documentElement;
            var courses = response.getElementsByTagName('Course');

            for(var course = 0; course < courses.length; ++course)
            {
                var newcourse = document.createElement('option');
                newcourse.text = courses[course].getAttribute("Section") + ": " + courses[course].getAttribute("Title");
                newcourse.value = courses[course].getAttribute("CallNumber");
                newcourse['courseinfo'] = courses[course];

                courselist_arr.push(newcourse);

                try {
                    courseselect.add(newcourse, null);
                } catch(ex) {
                    courseselect.add(newcourse);
                }
            }
        }
        else
        {
            alert("There was a problem retrieving the XML data:\n" + req.statusText);
        }
        courseselect.className = "";

        if(loadingbox !== null)
            loadingbox.className = "";

        do_filtering();
    }
    else
    {
        courseselect.className = "loading";
        if(loadingbox !== null)
            loadingbox.className = "loading";
    }
}

function courseClear()
{
    var courseselect = document.getElementById('courselist');
    // clear out the courses
    for(var courseopt = 0; courseopt < courseselect.options.length; )
    {
        if(courseopt == 'length')
            break;
        courseselect.remove(courseopt);
    }
}

function termChange()
{
    var termselect = document.getElementById("termlist");
    var termcode = termselect.options[termselect.selectedIndex].value;
    var courseselect = document.getElementById('courselist');
    // destroy all unsaved classes
    DestroyUnsaved();
    // clear out the course list
    courseClear(); // clear the box
    courselist_arr = []; // clear the array
    document.getElementById("course-search").value = "Search...";
    document.getElementById("course-search").className = "default";
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    // branch for IE/Windows ActiveX version
    } else if (window.ActiveXObject) {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = processCourseReqChange;
    req.open("GET", "core/core.php?cmd=getxml&term=" + termcode, true);
    req.send(null);
}

function processTermReqChange()
{
    if(req.readyState == 4)
    {
        if(req.status == 200)
        {
            response = req.responseXML.documentElement;
            var terms = response.getElementsByTagName('Term');
            termselect = document.getElementById("termlist");
            termselect.remove(0);
            for(var term = 0; term < terms.length; ++term)
            {
                newopt = document.createElement("option");
                newopt.value = terms[term].getAttribute('Code');
                newopt.text = terms[term].getAttribute('Name') + " (" + newopt.value + ")";
                if(newopt.value == start_term)
                    newopt.selected = true;
                try {
                    termselect.add(newopt, null);
                } catch(ex) {
                    termselect.add(newopt);
                }
            }
            termselect.selectedIndex = termselect.options.length - 1;
            if (window.XMLHttpRequest) {
                req = new XMLHttpRequest();
            // branch for IE/Windows ActiveX version
            } else if (window.ActiveXObject) {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            //req.onreadystatechange = processCourseReqChange;
            termChange();
        }
        else
        {
            alert("There was a problem retrieving the XML data...\n" + req.statusText);
        }
    }
}

document.getElementById("course-search").value = "Search...";

document.getElementById("course-search").onfocus = function()
{
    this.className = "";
    if(this.value == "Search...")
        this.value = "";
}

document.getElementById("course-search").onblur = function()
{
    if(this.value == "")
    {
        this.className = "default";
        this.value = "Search...";
    }
}

function do_filtering()
{
    var courseselect = document.getElementById('courselist');
    var searchbox = document.getElementById('course-search');
    var closed = document.getElementById('closed-checkbox');
    var cancelled = document.getElementById('cancelled-checkbox');
    var conflicts = document.getElementById('conflicts-checkbox');

    // clear out the course select box
    courseClear();

    for(var course = 0; course < courselist_arr.length; ++course)
    {
        courseinfo = courselist_arr[course]['courseinfo'];
        if(
            (searchbox.value == "Search..."
                || courseinfo.getAttribute('Title').toLowerCase().indexOf(
                    searchbox.value.toLowerCase()) != -1
                || courseinfo.getAttribute('Instructor1').toLowerCase().indexOf(
                    searchbox.value.toLowerCase()) != -1
                || courseinfo.getAttribute('CallNumber').indexOf(
                    searchbox.value) != -1
                || courseinfo.getAttribute('Section').toLowerCase().indexOf(
                    searchbox.value.toLowerCase()) != -1
                )
            && (closed.checked || courseinfo.getAttribute('Status') != 'C')
            && (cancelled.checked || courseinfo.getAttribute('Cancelled') != 'X')
            )
        {
            try {
                courseselect.add(courselist_arr[course], null);
            } catch(ex) {
                courseselect.add(courselist_arr[course]);
            }
        }
    }
}

var filtering_timeout = 0;

document.getElementById("course-search").onkeyup = function()
{
    clearTimeout(filtering_timeout);
    filtering_timeout = setTimeout('do_filtering();', 200);
}

document.getElementById('closed-checkbox').onchange = document.getElementById('cancelled-checkbox').onchange = document.getElementById('conflicts-checkbox').onchange = do_filtering;

var start_term = null;

function downloadTerms_callback(term)
{
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    // branch for IE/Windows ActiveX version
    } else if (window.ActiveXObject) {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    start_term = term;
    req.onreadystatechange = processTermReqChange;
    req.open("GET", "core/core.php?cmd=terms", true);
    req.send(null);
}

Persist.init(downloadTerms_callback);
