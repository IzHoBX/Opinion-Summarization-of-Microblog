import * as WebBrowser from 'expo-web-browser';
import * as React from 'react';
import { Image, Platform, StyleSheet, Text, TextInput, TouchableOpacity, View, Dimensions, Container } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';
import DropdownMenu from 'react-native';

import { MonoText } from '../components/StyledText';
import Posts from "../Posts.js"


export default function HomeScreen({ navigation }) {
  const [state, setState] = React.useState({posts:[]})
  const [positive, setPositive] = React.useState([])
  const [neutral, setNeutral] = React.useState([])
  const [negative, setNegative] = React.useState([])
  const [all, setAll] = React.useState([])

  React.useEffect(() => {
    function pullData() {
      var Httpreq = new XMLHttpRequest(); // a new request
      Httpreq.open("GET","http://localhost:7777/positive",false);
      Httpreq.send(null);
      var res = JSON.parse(Httpreq.responseText)["res"];
      setState({posts:res})
    }
    pullData()
  }, []);

  const [value, onChangeText] = React.useState('Useless Placeholder');

  return (
    <View style={styles.container} id="demo">
      <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
        <View style = {{
              flex: 1,
              justifyContent: 'center',
              flexDirection: 'row'
           }}>
          <TouchableOpacity style ={styles.positiveButton} onPress={()=> {
            console.log("positive")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/positive",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
            <Text style={styles.buttonText}> Positive</Text>
          </TouchableOpacity>
          <TouchableOpacity style ={styles.neutralButton} onPress={()=>{
            console.log("neutral")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/neutral",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
            <Text style={styles.buttonText}> Neutral</Text>
          </TouchableOpacity>
          <TouchableOpacity style ={styles.negativeButton} onPress={()=> {
            console.log("negative")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/negative",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
            <Text style={styles.buttonText}> Negative</Text>
          </TouchableOpacity>
          <TouchableOpacity style ={styles.allButton} onPress={()=>{
            console.log("all")
            var Httpreq = new XMLHttpRequest(); // a new request
            Httpreq.open("GET","http://localhost:7777/all",false);
            Httpreq.send(null);
            var res = JSON.parse(Httpreq.responseText)["res"];
            setState({posts:res})
            }}>
            <Text style={styles.buttonText}> All</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.welcomeContainer}>
          <Image
            source={
              __DEV__
                ? require('../assets/images/chat2.png')
                : require('../assets/images/chat2.png')
            }
            style={styles.welcomeImage}
          />

        </View>
        <View style={styles.getStartedContainer}>

          <Text style={styles.getStartedText}>Welcome</Text>

          <Posts posts={state.posts}/>

        </View>
        </ScrollView>
    </View>
  );
}

function DevelopmentModeNotice() {
  if (__DEV__) {
    const learnMoreButton = (
      <Text onPress={handleLearnMorePress} style={styles.helpLinkText}>
        Learn more
      </Text>
    );

    return (
      <Text style={styles.developmentModeText}>
        Development mode is enabled: your app will be slower but you can use useful development
        tools. {learnMoreButton}
      </Text>
    );
  } else {
    return (
      <Text style={styles.developmentModeText}>
        You are not in development mode: your app will run at full speed.
      </Text>
    );
  }
}

function handleLearnMorePress() {
  WebBrowser.openBrowserAsync('https://docs.expo.io/versions/latest/workflow/development-mode/');
}

function handleHelpPress() {
  WebBrowser.openBrowserAsync(
    'https://docs.expo.io/versions/latest/get-started/create-a-new-app/#making-your-first-change'
  );
}

const data = ["neutral", "positive", "negative"]

const styles = StyleSheet.create({
  positiveButton: {
    backgroundColor: 'green',
  },
  neutralButton: {
    backgroundColor: 'grey',
    marginLeft: 15
  },
  negativeButton: {
    backgroundColor: 'red',
    marginLeft: 15
  },
  allButton: {
    backgroundColor: 'yellow',
    marginLeft: 15
  },
  buttonText: {
    fontSize: 17,
    color: 'black',
    lineHeight: 24,
    textAlign: 'center',
  },
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  developmentModeText: {
    marginBottom: 20,
    color: 'rgba(0,0,0,0.4)',
    fontSize: 14,
    lineHeight: 19,
    textAlign: 'center',
  },
  contentContainer: {
    paddingTop: 30,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 20,
  },
  welcomeImage: {
    width: 100,
    height: 80,
    resizeMode: 'contain',
    marginTop: 3,
    marginLeft: -10,
  },
  getStartedContainer: {
    alignItems: 'center',
  },
  getStartedText: {
    fontSize: 17,
    color: 'rgba(96,100,109, 1)',
    lineHeight: 24,
    textAlign: 'center',
  },
  helpLinkText: {
    fontSize: 14,
    color: '#2e78b7',
  },
  scrollContainer: {
    flex: 1,
  },
  box: {
    width: 150,
    height: 20,
    marginLeft: 15,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'grey',
  }
});
/*
<View style= {styles.scrollContainer}>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box1</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box2</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box3</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box4</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box5</Text></View>
  <View style ={styles.box}><Text style={styles.getStartedText}> Box6</Text></View>
</View>*/
