// Set on load page callback
document.addEventListener("DOMContentLoaded", function() {
    const elem = document.querySelector("form");
    const selectedTargetLanguagesCountMax = elem.getAttribute("data-selected-target-languages-count-max");

    let selectedTargetLanguages = [];
    let selectedTargetLanguagesCount = 0;
    const nodeList = document.querySelectorAll(".select-target-language");
    for (let i = 0; i < nodeList.length; i++) {
        nodeList[i].checked = false;
        nodeList[i].value = nodeList[i].id;

        nodeList[i].onchange = (e) => {
            if (! e.target.checked ) {
                selectedTargetLanguagesCount--;
                ret = unselectTargetLanguage(e.target, selectedTargetLanguages);
                selectedTargetLanguages = ret["selectedTargetLanguages"]; 
                e.target.value = ret["value"];
            }
            else {
                if (selectedTargetLanguagesCount < selectedTargetLanguagesCountMax) {
                    selectedTargetLanguagesCount++;
                    ret = selectTargetLanguage(e.target, selectedTargetLanguages);
                    selectedTargetLanguages = ret["selectedTargetLanguages"]; 
                    e.target.value = ret["value"];
                }
                else {
                    e.target.checked = false;
                }
            } 

            showSelectedTargetLanguages(selectedTargetLanguages)
        };
    }
        
    showSelectedTargetLanguages(selectedTargetLanguages)
});


function unselectTargetLanguage(targetElem, selectedTargetLanguages) {
    const ret = {};

    const value = targetElem.id;
    ret["value"] = value;

    for (let i = 0; i < selectedTargetLanguages.length; i++) {
        if (selectedTargetLanguages[i].id == targetElem.id) {
            selectedTargetLanguages.splice(i, 1);
        }
    }

    const elem = document.querySelector("form");
    const languageToSortNumberSeparator = elem.getAttribute("data-language-to-sort-number-separator");

    for (let i = 0; i < selectedTargetLanguages.length; i++) {
        const value = selectedTargetLanguages[i].id + languageToSortNumberSeparator + i;
        selectedTargetLanguages[i].value = value;
    }

    ret["selectedTargetLanguages"] = selectedTargetLanguages; 

    return ret;
}


function selectTargetLanguage(targetElem, selectedTargetLanguages) {
    const ret = {};

    const elem = document.querySelector("form");
    const languageToSortNumberSeparator = elem.getAttribute("data-language-to-sort-number-separator");

    const value = targetElem.id + languageToSortNumberSeparator + selectedTargetLanguages.length;
    ret["value"] = value;

    selectedTargetLanguages.push(targetElem);

    ret["selectedTargetLanguages"] = selectedTargetLanguages; 

    return ret;
}


function showSelectedTargetLanguages(selectedTargetLanguages) {
    console.log(selectedTargetLanguages);

    for (let i = 0; i < selectedTargetLanguages.length; i++) {
        console.log(selectedTargetLanguages[i].name, selectedTargetLanguages[i].value);
    }   
}
