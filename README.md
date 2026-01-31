WARNING: I TAKE NO RESPONSIBILITY FOR THE USE OF THIS PROJECT BY ANY THIRD PARTY! BE ADVICED IT CONTAINS ELECTRICAL AND CLOUD COMPONENTS. USE AT YOUR OWN PERIL!

To run the IOT project:

\- Go to AWS Management Console -> Lambda -> select a lambda -> Configurations -> Concurrency and recursion detection -> under Concurrency, click Edit -> Check "Use unreserved account concurrency" -> Click save.

\- Do the same for the other lambdas.

\- Go to CloudFront -> check the distribution and click Enabled -> Wait until deployed.

\- Wire the electric board to the Raspberry Pi with one wire connected to the + cathode and to the GPIO 7 pin on the Raspberry Pi (inner row \[close to the center of the Raspberry Pi], 4th pin) and a second wire connected to the - cathode and to GPIO 6 pin on the Raspberry Pi (GND - outer row, far from the center, 3rd pin).

\- Run the hardware\_controller.py file via Thonny (Raspberry Pi's built in text editor). Wait till it shows that it's connected to AWS IoT. You may need to install the package for push notifications (maho-mqtt).

\- Go to AWS CloudFront, click on the distribution and copy paste the domain name into the browser. That would open the web application. Click the button, and you'll see that the Raspberry Pi receives the message and changes the hardware accordingly.



To shut everything down after using the IOT system (keep things safe):

\- Go to AWS Management Console -> Lambda -> select a lambda -> Configurations -> Concurrency and recursion detection -> under Concurrency, click Edit -> Check "Reserve concurrency", set to 0 and click Save.

\- Do the same for the other lambdas.

\- Go to CloudFront -> check the distribution and click Disabled.

\- To shutdown the Raspberry Pi, open the terminal and type Shutdown. Don't detach from electricity before the system performed an orderly shutdown.

