## Table of contents
* [General info](#general-info)
* [Output](#output)
* [Setup](#setup)

## General info
An attempt to create a Summary of Long and logs of Product Reviews.    
The provided Model and Steps give the following output(For understanding) of the given terrible review.    


## Output Example

#### **`Review:`**
```
Review 1:  
'Amazing camera quality expected  battery also good performance  Display  body  touch experience best Ive ever   
Sound quality speakers sufficient  Apple known customer friendly security services see  processor best work  
  would definitely recommend everyone looking  go without delay  amazing thing delivery  Flipkart delivered span'

Review 2:
Camera is Great but Battery is Bad.
```

#### **`Output:`**

  For Review 1:
```python
  Aspects:
  {'camera quality', 'battery', 'security services', 'processor', 'delivery'}
```

  For Review 2:
```python
  Aspects:
  {'Camera', 'Battery'}
```

  For Review 1:
```python
  Aspects with context:

  {'camera quality': 'camera quality expected',
 'battery': 'battery also good',
 'security services': 'security services see',
 'processor': 'processor best',
 'delivery': 'delivery Flipkart delivered span'}
```

  For Review 2:
```python
  Aspects with Context:

  {
  'Camera' : 'Camera is Great',
  'Battery': "Battery is Bad"
  }
```
Final Output is Aspect with Context, Aspect is given to highlight the importance of Aspect Extraction for finding the context.

## Setup
Packages: 
```python
!pip install pyabsa -U
```
Run the model on GPU if it crashes.  
  
Modules Required:  
- PyTorch
- Transformers
- SpaCy
- Pyabsa
- Python



