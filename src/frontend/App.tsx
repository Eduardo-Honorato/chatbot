import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, Button, ScrollView, StyleSheet, Alert } from 'react-native';

const App = () => {
  const [screen, setScreen] = useState<'chat' | 'search'>('chat');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [searchResults, setSearchResults] = useState[];
  const [searchQuery, setSearchQuery] = useState('');

  const navigateTo = (screen: 'chat' | 'search') => {
    setScreen(screen);
    setMessage('');
    setSearchQuery('');
    setSearchResults([]);
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    setMessages(prev => [...prev, { role: 'user', content: message }]);
    setMessage('');

    // TODO: Send to backend API
    // For now, simulate a response
    const response = `Você disse: "${message}"`;
    setMessages(prev => [...prev, { role: 'assistant', content: response }]);
  };

  const performSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearchResults([]); // Clear previous results
    // TODO: Call backend search endpoint
    // For now, simulate results
    setSearchResults([
      { title: 'Documentação Python', excerpt: 'Guia completo da linguagem Python' },
      { title: 'Flask Tutorial', excerpt: 'Como criar APIs com Flask' },
    ]);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Chatbot Assistente</Text>
      </View>

      <View style={styles.contentArea}>
        {screen === 'chat' && (
          <View>
            <ScrollView style={styles.messageList} scrollEventThrottle={100}>
              {messages.map((msg, index) => (
                <View key={index} style={styles.messageBubble}>
                  <Text style={{ ...styles.text, alignSelf: msg.role === 'assistant' ? 'flex-end' : 'flex-start' }}>
                    {msg.role}: {msg.content}
                  </Text>
                </View>
              ))}
            </ScrollView>

            <View style={styles.inputArea}>
              <TextInput
                placeholder="Digite sua mensagem..."
                value={message}
                onChangeText={setMessage}
                style={styles.input}
                multiline
                numberOfLines={4}
              />
              <Button title="Enviar" onPress={sendMessage} style={styles.sendButton} />
            </View>
          </View>
        )}

        {screen === 'search' && (
          <View>
            <View style={styles.searchArea}>
              <TextInput
                placeholder="Buscar documentação..."
                value={searchQuery}
                onChangeText={setSearchQuery}
                style={styles.input}
                placeholderTextColor="#aaa"
              />
              <Button title="Buscar" onPress={performSearch} style={styles.searchButton} />
            </View>

            {searchResults.length > 0 && (
              <ScrollView style={styles.resultList}>
                {searchResults.map((result, index) => (
                  <View key={index} style={styles.resultItem}>
                    <Text style={styles.resultTitle}>{result.title}</Text>
                    <Text style={styles.resultExcerpt}>{result.excerpt}</Text>
                  </View>
                ))}
              </ScrollView>
            )}

            {searchResults.length === 0 && searchQuery.trim().length > 0 && (
              <Text style={styles.noResults}>Nenhum resultado encontrado</Text>
            )}
          </View>
        )}
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
    paddingTop: Platform.constants?.statusBarHeight || 20,
  },
  headerTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  contentArea: {
    flex: 1,
    padding: 16,
  },
  messageList: {
    flex: 1,
    marginBottom: 20,
  },
  messageBubble: {
    padding: 12,
    borderRadius: 12,
    marginBottom: 12,
    maxWidth: '80%',
  },
  text: {
    fontSize: 14,
    lineHeight: 18,
  },
  inputArea: {
    flexDirection: 'row',
    marginTop: 10,
    paddingBottom: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 20,
    overflow: 'hidden',
  },
  input: {
    flex: 1,
    padding: 10,
    fontSize: 14,
    color: '#333',
  },
  sendButton: {
    backgroundColor: '#0066cc',
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  searchArea: {
    marginBottom: 20,
    padding: 12,
    backgroundColor: '#fafafa',
    borderRadius: 8,
  },
  searchButton: {
    marginLeft: 10,
    backgroundColor: '#0066cc',
    paddingHorizontal: 15,
    paddingVertical: 5,
  },
  resultList: {
    marginTop: 10,
  },
  resultItem: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    backgroundColor: '#fff',
  },
  resultTitle: {
    fontWeight: 'bold',
    fontSize: 14,
  },
  resultExcerpt: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  noResults: {
    color: '#888',
    fontSize: 14,
    marginTop: 20,
  },
});

export default App;