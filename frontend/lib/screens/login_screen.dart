import 'package:flutter/material.dart';
import '../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  
  bool _isLoading = false;
  bool _isLoginMode = true;
  final _formKey = GlobalKey<FormState>();

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      if (_isLoginMode) {
        // LOGOWANIE
        final response = await ApiService.login(
          _usernameController.text,
          _passwordController.text,
        );
        
        // Sukces - przechodzimy do home screen
        Navigator.pushReplacementNamed(
          context,
          '/home',
          arguments: response['access_token'],
        );
      } else {
        // REJESTRACJA
        final response = await ApiService.register(
          _usernameController.text,
          _emailController.text,
          _passwordController.text,
        );
        
        // Po rejestracji automatycznie logujemy
        final loginResponse = await ApiService.login(
          _usernameController.text,
          _passwordController.text,
        );
        
        Navigator.pushReplacementNamed(
          context,
          '/home',
          arguments: loginResponse['access_token'],
        );
      }
    } catch (e) {
      _showErrorSnackBar(_isLoginMode ? 'Błąd logowania: $e' : 'Błąd rejestracji: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showErrorSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: Duration(seconds: 3),
      ),
    );
  }

  void _switchAuthMode() {
    setState(() {
      _isLoginMode = !_isLoginMode;
      // Czyść pola przy zmianie trybu
      if (!_isLoginMode) {
        _emailController.clear();
      }
    });
  }

  String? _validateEmail(String? value) {
    if (!_isLoginMode && (value == null || value.isEmpty)) {
      return 'Wprowadź email';
    }
    if (!_isLoginMode && !value!.contains('@')) {
      return 'Wprowadź poprawny email';
    }
    return null;
  }

  String? _validateUsername(String? value) {
    if (value == null || value.isEmpty) {
      return 'Wprowadź nazwę użytkownika';
    }
    if (value.length < 3) {
      return 'Nazwa użytkownika musi mieć co najmniej 3 znaki';
    }
    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Wprowadź hasło';
    }
    if (value.length < 6) {
      return 'Hasło musi mieć co najmniej 6 znaków';
    }
    return null;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isLoginMode ? 'Logowanie' : 'Rejestracja'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Logo/Header
              Icon(
                Icons.account_balance_wallet,
                size: 80,
                color: Colors.blue,
              ),
              SizedBox(height: 20),
              Text(
                'Apka Finansowa',
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: Colors.blue,
                ),
              ),
              SizedBox(height: 8),
              Text(
                _isLoginMode 
                  ? 'Zaloguj się do swojego konta' 
                  : 'Załóż nowe konto',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey,
                ),
              ),
              SizedBox(height: 40),

              // Pole nazwy użytkownika
              TextFormField(
                controller: _usernameController,
                decoration: InputDecoration(
                  labelText: 'Nazwa użytkownika',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
                validator: _validateUsername,
              ),
              SizedBox(height: 16),

              // Pole email (tylko przy rejestracji)
              if (!_isLoginMode) ...[
                TextFormField(
                  controller: _emailController,
                  decoration: InputDecoration(
                    labelText: 'Email',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.email),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: _validateEmail,
                ),
                SizedBox(height: 16),
              ],

              // Pole hasła
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Hasło',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.lock),
                ),
                validator: _validatePassword,
              ),
              SizedBox(height: 32),

              // Przycisk submit
              _isLoading
                  ? CircularProgressIndicator()
                  : ElevatedButton(
                      onPressed: _submit,
                      child: Text(
                        _isLoginMode ? 'ZALOGUJ SIĘ' : 'ZAREJESTRUJ SIĘ',
                        style: TextStyle(fontSize: 16),
                      ),
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size(double.infinity, 50),
                        backgroundColor: Colors.blue,
                        foregroundColor: Colors.white,
                      ),
                    ),

              SizedBox(height: 20),

              // Przełącznik trybu
              TextButton(
                onPressed: _isLoading ? null : _switchAuthMode,
                child: Text(
                  _isLoginMode 
                    ? 'Nie masz konta? Zarejestruj się' 
                    : 'Masz już konto? Zaloguj się',
                  style: TextStyle(
                    color: Colors.blue,
                    fontSize: 16,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    _emailController.dispose();
    super.dispose();
  }
}