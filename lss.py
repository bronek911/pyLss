from flask import Flask, render_template
from serial import Serial
import time

app = Flask(__name__)

arduino = Serial("/dev/ttyUSB0", 57600, timeout=1)

@app.route("/laser-on/<num>")
def laser(num):
    arduino.write(bytes('M71T'+num, 'utf-8'))
    return 'True'

@app.route('/reset')
def resetStepper():
    arduino.write(bytes('G50', 'utf-8'))
    return 'True'

@app.route('/move/<steps>')
def actionMove(steps):

    # move(steps)

    while True:

        stringStr = ''
        arduino.write(bytes('G1X' + str(steps), 'utf-8'))
        time.sleep(0.1) #wait for arduino to answer
        while arduino.inWaiting()==0: pass
        if  arduino.inWaiting()>0:


            answer = arduino.readline()
            while answer:
                if(answer.decode("utf-8") == 'ok'):
                    return render_template("index.html", string=answer.decode("utf-8"))
                answer = arduino.readline()


            # answer = arduino.readline()
            # while answer:
            #     bytesStr = arduino.readline()
            #     if(bytesStr.decode("utf-8") == 'ok'):
            #         return render_template("index.html", string=bytesStr.decode("utf-8"))

    # show the post with the given id, the id is an integer
    return 'True'
    
def move(steps):

    string = 'G1X'
    string += str(steps)
    arduino.write(bytes(string, 'utf-8'))

    # show the post with the given id, the id is an integer
    return 'True'


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True, port=8082)