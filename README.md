I created this to make the process of adding custom operation commands a little easier by streamlining the creation of the necessary XML structure.

Usage key:
### Command separator - //
 - This will be used to separate commands. For instanace, if you wanted the VyOS command to be "show device detail", you would type show//device//detail
### Node Types:
 - If you type a normal word, it will default to a normal node
 - tagNode: Encapsulate the word in <>. Example: 'show//\<device\>//detail' will make 'device' a tagNode, and make the actual command "show device \<name of device\> detail"
 - leafNode: Start the name with a '!' to define the value as a leafNode. Example: 'show//\<device\>//!detail' will make the node types in order node/tagNode/leafNode
### Calling values under a node:
 - '@': The use of the '@' operator attached to a node name tells the script that there will be values directly within that nodes hierarchy. Example: 'show//device@properties'
 - ':': The use of the ':' operator denotes the value before it should be directly under the node. Example: 'show//device@properties:' will add <properties/> directly under the 'device' node.
 - ',': The use of the ',' operator allows you to separate additional values that are being added: Example: 'show//device@properties:help,moreHelp'
 - '=": The use of the '=' operator allows a value to be added to the item you're defining: Example: 'show//device@properties:help=Show Devices'

### Usage Examples:
show firewall ipv4 detail (basic outline) - show//firewall//ipv4//detail
```xml
Enter your command: show//firewall//ipv4//detail
<?xml version="1.0" ?>
<interfaceDefinition>
  <node name="show">
    <children>
      <node name="firewall">
        <children>
          <node name="ipv4">
            <children>
              <node name="detail"/>
            </children>
          </node>
        </children>
      </node>
    </children>
  </node>
</interfaceDefinition>
```

show firewall ipv4 detail (with helpers and detail as leafNode) - show//firewall@properties:help=Show firewall information//ipv4@properties:help=Show IPv4 firewall//!detail@properties:help=Show list view of IPv4 forward filter firewall rules:completionHelp:path=firewall ipv4 forward filter rule detail@command:=insert some command
```xml
<?xml version="1.0" ?>
<interfaceDefinition>
  <node name="show">
    <children>
      <node name="firewall">
        <properties>
          <help>Show firewall information</help>
        </properties>
        <children>
          <node name="ipv4">
            <properties>
              <help>Show IPv4 firewall</help>
            </properties>
            <children>
              <leafNode name="detail">
                <properties>
                  <help>Show list view of IPv4 forward filter firewall rules</help>
                  <completionHelp>
                    <path>firewall ipv4 forward filter rule detail</path>
                  </completionHelp>
                </properties>
                <command>insert some command</command>
              </leafNode>
            </children>
          </node>
        </children>
      </node>
    </children>
  </node>
</interfaceDefinition>
```
