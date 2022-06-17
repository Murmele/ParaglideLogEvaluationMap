# Paraglide log evaluation

Evaluate your .IGC/.igc files to gain your skills. The result is a map with the flight and colorized to show the climbrate at specific locations. For an interactive result download the file [Features_0.html](https://github.com/Murmele/ParaglideLogEvaluationMap/blob/master/ExampleResults/Features_0.html) and open it in your browser.

![Result](https://github.com/Murmele/ParaglideLogEvaluationMap/raw/master/Screenshots/Result.png)

## Prerequirements
- Python (See Pipfile for required version)
- Pipenv (pip install pipenv)

## Usage
1) Change to source folder
2) Install pipenv environment `pipenv install`
3) Execute script: `pipenv run python igcLogEvaluation.py <relative path/file>`
Where <relative path/file> can be a list of relative paths or relative filenames

## Example
```
pipenv run python igcLogEvaluation.py TestData
```
This plots all logs inside of the TestData folder

