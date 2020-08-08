# LightWare DIY #

API and SPA for controlling LED lamps and dimmable LED lamps (simple home automation)

    [x] manage GPIO on Banana Pro board (over sysfs)
    [x] send data over i2c (remote control Krida Electronics dimmer)
    [x] service-worker support
    [x] use semantic UI framework
   
## Screenshot ##

![LightWare Screenshot](media/screenhot_lightware.png?raw=true "Screenshot")

## Device photo ##

![LightWare](media/lightware.jpg?raw=true "LightWare")
Banana Pro + solid state relay + Krida Electronics i2c dimmer 


![Krida dimmer](media/dimmer.jpg?raw=true "Krida dimmer")
Krida Electronics i2c dimmer 

## Links
[Samsung smart things hubaction](https://docs.smartthings.com/en/latest/ref-docs/hubaction-ref.html)


```python
def json = new JsonBuilder()
json.call("command":"${command}","password":"${settings.hostpassword}")

def headers = [:] 
headers.put("HOST", "$host:$port")
headers.put("Content-Type", "application/json")

log.debug "The Header is $headers"

def method = "POST"

try {
    def hubAction = new physicalgraph.device.HubAction(
        method: method,
        path: path,
        body: json,
        headers: headers,
    )
   
    log.debug hubAction
    hubAction
}
catch (Exception e) {
    log.debug "Hit Exception $e on $hubAction"
}

```