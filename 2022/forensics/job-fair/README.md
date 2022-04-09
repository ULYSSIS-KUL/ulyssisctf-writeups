# job-fair writeup

The flavortext mentions that you have to add the event to your calendar. You could do this by scanning the QR code on the poster. This QR code is an iCalendar `VEVENT` calendar component of which the `DESCRIPTION` property contains the flag. Many QR code scanners and calendar apps don't show the `DESCRIPTION` field. You can still see the flag by inspecting the raw QR code data.