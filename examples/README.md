# Running the Code Locally

## 1. Clone the Git Repository
To get started, clone the Git repository using the following command:

```
git clone https://github.com/shivam096/dinero.git
```

## 2. Setting Up the Local Environment
1. Create a new conda environment based on the specifications provided in a YAML file [environment.yml](environment.yml).
```
conda env create -f environment.yml
```
2. Activate the conda environment
```
conda activate dinero_env
```

3. Remember to deactivate the Conda environment after running the code inside this environment:
```
conda deactivate
```

## 3. Running the Streamlit Application
Navigate to the cloned repository:
```
cd dinero
```
Then run the Streamlit application with the dark theme:
```
streamlit run app.py --theme.base dark
```
The application will open up in your browser on -
    Local URL : http://localhost:8501
    Network URL : http://10.0.0.187:8501


# RUNNING THE CODE AS A PACAKGE

1. Build the Package
Execute the following command to build the package:
```
python -m build
```
This command will generate a zip file under the root directory in the `dist` folder.

## 2. Install the Package
Install the generated zip file using pip with the following command:
2.
```
pip install <path/to/zip/file>
```

3. Import each module from the root directory
Ex -
```
from dinero.backend.stock_data_manager import download_stock_data
```

For detailed instructions on how to use the stock analysis tool, refer to the [tool guide document](tool_guide_for_user.md).







