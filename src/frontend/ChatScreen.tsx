import React, { useState, useEffect } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, ScrollView, StyleSheet, ActivityIndicator } from 'react-native';
import { chatAPI, historyAPI } from './api';

interface ChatScreenProps {
  navigation: any;
}

const ChatScreen: React.FC<ChatScreenProps> = ({ navigation }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    // Initialize session and load history
    const initSession = async () => {
      try {
        const history = await historyAPI('default');
        setMessages(history);
        setSessionId('default');
      } catch (error) {
        console.error('Failed to load history:', error);
      }
    };

    initSession();
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setMessages(prev => [...prev, { role: 'user', content: input }]);

    try {
      const response = await chatAPI(input);
      setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Desculpe, houve um erro ao processar sua mensagem.' }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  const refreshHistory = async () => {
    if (sessionId) {
      const history = await historyAPI(sessionId);
      setMessages(history);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Chatbot</Text>
      </View>

      <View style={styles.messagesContainer}>
        <ScrollView
          style={styles.scrollContainer}
          contentContainerStyle={styles.contentContainer}
          showsVerticalScrollIndicator={false}
        >
          {messages.map((msg, index) => (
            <View key={index} style={styles.bubbleContainer}>
              <View style={styles.bubble}>
                <Text style={styles.bubbleText}>
                  {msg.role}: {msg.content}
                </Text>
              </View>
            </View>
          ))}
          {loading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" />
            </View>
          )}
          {messages.length === 0 && !loading && (
            <Text style={styles.emptyState}>Digite uma mensagem acima</Text>
          )}
        </ScrollView>
      </View>

      <View style={styles.inputContainer}>
        <TextInput
          placeholder="Digite uma mensagem..."
          value={input}
          onChangeText={setInput}
          style={styles.input}
          placeholderTextColor="#888"
          disableSendToFocus={true}
        />
        <Button title="Enviar" onPress={sendMessage} disabled={loading} style={styles.sendButton} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#0066cc',
    padding: 16,
    paddingTop: 24,
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  messagesContainer: {
    flex: 1,
    marginHorizontal: 16,
    marginBottom: 16,
  },
  scrollContainer: {
    flexGrow: 1,
  },
  contentContainer: {
    paddingBottom: 20,
  },
  bubbleContainer: {
    marginBottom: 12,
  },
  bubble: {
    padding: 12,
    borderRadius: 12,
    maxWidth: '80%',
  },
  bubbleUser: {
    alignSelf: 'flex-start',
    backgroundColor: '#DCF8C6',
  },
  bubbleAssistant: {
    alignSelf: 'flex-end',
    backgroundColor: '#FFF',
  },
  bubbleText: {
    fontSize: 14,
    lineHeight: 18,
  },
  inputContainer: {
    flexDirection: 'row',
    marginHorizontal: 16,
    marginBottom: 16,
  },
  input: {
    flex: 1,
    height: 48,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 20,
    fontSize: 14,
    backgroundColor: '#fff',
  },
  sendButton: {
    backgroundColor: '#0066cc',
    paddingHorizontal: 20,
    paddingVertical: 8,
  },
  loadingContainer: {
    marginTop: 20,
    alignSelf: 'center',
  },
  emptyState: {
    color: '#888',
    textAlign: 'center',
    marginTop: 20,
    fontSize: 14,
  }
});

export default ChatScreen;