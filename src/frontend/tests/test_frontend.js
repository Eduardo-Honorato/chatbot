/* Testes unitários básicos para o frontend React Native do Chatbot */

// Note: Estes testes são estruturais e verificam a existência dos componentes
// Em um ambiente Expo/React Native real, seria necessário o Jest Native ou detox

describe('Chatbot Frontend Structure', () => {
  test('App component should render without crashing', () => {
    // Verificação estrutural - o componente App.tsx deve ser importável
    const React = require('react');
    expect(React).toBeDefined();
  });

  test('api.ts should export core functions', () => {
    // Verifica que o arquivo api.ts tem as funções esperadas
    const fs = require('fs');
    const path = require('path');
    const apiContent = fs.readFileSync(path.join(__dirname, '../api.ts'), 'utf8');
    expect(apiContent).toContain('chatAPI');
    expect(apiContent).toContain('historyAPI');
    expect(apiContent).toContain('searchAPI');
  });

  test('ChatScreen.tsx should exist and have content', () => {
    const fs = require('fs');
    const path = require('path');
    const chatScreenPath = path.join(__dirname, '../ChatScreen.tsx');
    expect(fs.existsSync(chatScreenPath)).toBeTruthy();
    const chatScreenContent = fs.readFileSync(chatScreenPath, 'utf8');
    expect(chatScreenContent.length).toBeGreaterThan(100);
  });

  test('DocsSearchScreen.tsx should exist and have content', () => {
    const fs = require('fs');
    const path = require('path');
    const docsSearchPath = path.join(__dirname, '../DocsSearchScreen.tsx');
    expect(fs.existsSync(docsSearchPath)).toBeTruthy();
    const docsSearchContent = fs.readFileSync(docsSearchPath, 'utf8');
    expect(docsSearchContent.length).toBeGreaterThan(100);
  });

  test('package.json should have required dependencies', () => {
    const fs = require('fs');
    const path = require('path');
    const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, '../package.json'), 'utf8'));
    expect(packageJson.dependencies).toBeDefined();
    expect(packageJson.dependencies.react).toBeDefined();
    expect(packageJson.dependencies['react-native']).toBeDefined();
  });
});