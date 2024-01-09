## Table of contents
* [General info](#general-info)
* [Output](#output)
* [Setup](#setup)

## General info
An attempt to create a Summary of Long and logs of Product Reviews. For now, I have removed the scrapper for Amazon, Flipkart, and Croma for collecting the given Product because the Chrome driver is not stable and is not running on the new update, it will be added once the ChromeDriver gets a stable version release.
The provided Model and Steps give the following output(For understanding) of the given terrible review.    


## Output Example

#### **`Review:`**
```python
Review 1:  
'Amazing camera quality expected  battery also good performance  Display  body  touch experience best Ive ever   
Sound quality speakers sufficient  Apple known customer friendly security services see  processor best work  
  would definitely recommend everyone looking  go without delay  amazing thing delivery  Flipkart delivered span'
```

```python
Review 2:
Camera is Great but Battery is Bad.
```

#### **`Output:`**

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
  'Camera': 'Camera is Great',
  'Battery': "Battery is Bad"
  }
```
In the dictionary, Key is the Aspect of the Product, and Value is the context of the Aspect as given in the review.

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
- Selenium




