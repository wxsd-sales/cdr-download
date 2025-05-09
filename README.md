# CDR Download

Download CDRs from your org as local .csv files, or send SMS for "missed" calls.

* *missed* calls are defined by small call duration, local hangup, because remote voicemail shows as call answered in CDR.

## Demo
[![Vidcast Overview](https://github.com/user-attachments/assets/22255ed7-5c94-4365-9055-1dc044d1eff0)](https://app.vidcast.io/share/baa4c286-5d87-4fc7-b945-d6d2ac7bd3d3)


## Setup

### Prerequisites & Dependencies:

- Developed on MacOS Sequoia (15.3)
- Developed on Python 3.8.1 & 3.8.3
-   Other OS and Python versions may work but have not been tested

### Webex Connect:
If you want to send SMS for missed calls, you will need to import the ```webex-connect-simple-sms.workflow``` into a Webex Connect tenant flow.  If you do not have a Webex Connect environment, you can spin up a sandbox [here](https://cpaas.webex.com/products/webex-connect/sandbox).  
Please note, you will need to have an SMS enabled number in your Webex Connect tenant to send outbound SMS.   
1. You will need to edit the flow to ensure your JSON is being parsed by the Webhook (first) node.
2. You will need to edit the SMS (second) node to select the number from which you want to send the SMS.

### Installation Steps:

1. Create a Service App: https://developer.webex.com/my-apps/new
   With the scope: ```spark-admin:calling_cdr_read```
   The App will need to be approved in Control Hub, then a token can be generated using the ```client_secret```

2. Python 3 required
4. Clone this repository  
       Alternatively, you can download the files [cdr_puller.py](cdr_puller.py)and [example.env](example.env)  
5. ```pip install -r requirements.txt```  
        or manually install each requirement:  
        ```pip install python-dotenv```  
        ```pip install requests```  
6. Populate the ```CLIENT_ID```, ```CLIENT_SECRET``` and ```REFRESH_TOKEN``` with Service App values between the double quotes of each respective line in the file ```example.env```
7. Change ```BUSINESS_NAME``` to reflect the name of your business. This will appear in the SMS sent to remote end users who miss calls.
8. Populate the ```WEBEX_CONNECT_URL``` with the inbound webhook url setup in your WebexConnect workflow.
9. Rename the file ```example.env``` to ```.env```




### Run:
You can use either of the files to launch the application:
```
python cdr_puller_run_forever.py
```
or
```
python cdr_puller_run_once.py
```
Before you launch the script, please open the desired file and make sure the keyword parameters passed to the ```get_cdrs()``` function match your objective.  
For example, if you want to send SMS, but not write CSV:
```
data.get_cdrs(write_csv=False, send_missed_sms=True)
```


## License

All contents are licensed under the MIT license. Please see [license](LICENSE) for details.

## Disclaimer

<!-- Keep the following here -->  
Everything included is for demo and Proof of Concept purposes only. Use of the site is solely at your own risk. This site may contain links to third party content, which we do not warrant, endorse, or assume liability for. These demos are for Cisco Webex usecases, but are not Official Cisco Webex Branded demos.
 
 
## Support

Please contact the Webex SD team at [wxsd@external.cisco.com](mailto:wxsd@external.cisco.com?subject=CDRDownload) for questions. Or for Cisco internal, reach out to us on Webex App via our bot globalexpert@webex.bot & choose "Engagement Type: API/SDK Proof of Concept Integration Development". 
